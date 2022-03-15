from operator import itemgetter

from ..models import Recording, Account, UserMusic, MusicRecommendations
from ..serializers import RecordingSerializer, UserMusicRecommendationsSerializer, UserMusicIdSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator
from pandas import DataFrame
from numpy import matmul, fill_diagonal, absolute
from time import time_ns


@api_view(['GET', 'POST'])
def recommendation_list(request):
    user_id = request.user.id
    user_recommendations = MusicRecommendations.objects.filter(pk=user_id)
    if 'regenerate_recommendations' in request.data.keys() or not user_recommendations:
        recommendations_ids = generate_recommendations(user_id)
        if not user_recommendations:
            MusicRecommendations.objects.create(pk=user_id, recommendations=recommendations_ids)
        else:
            MusicRecommendations.objects.filter(pk=user_id).update(recommendations=recommendations_ids)
    else:
        recommendations_ids = user_recommendations.values()[0]['recommendations']

    query_set = Recording.objects.filter(id__in=recommendations_ids)
    recommendations = [query_set[y] for x in recommendations_ids for y in range(len(query_set)) if
                       query_set[y].id == x]

    serializer = RecordingSerializer(recommendations, many=True)
    return Response(serializer.data)


def get_similar_user_ids(user_id: int):
    if not len(UserMusic.objects.filter(account=user_id)):
        return None
    query_set = UserMusic.objects.all().exclude(like_status=0).values()
    serializer = UserMusicRecommendationsSerializer(query_set, many=True)
    df = DataFrame.from_records(serializer.data)
    pivot_table = df.pivot_table(index='account_id', columns='recording_id', values='like_status', fill_value=0,
                                 dropna=True)
    user_ids_ordered = pivot_table.index
    matrix = pivot_table.to_numpy()
    matrix_transposed = matrix.transpose()

    # Produce matrix of correlations between users; clear the diagonal as it shows one's similarity with themselves
    product = matmul(matrix, matrix_transposed)
    fill_diagonal(product, 0)

    id_range = range(len(user_ids_ordered))
    user_row_id = [x for x in id_range if user_ids_ordered[x] == user_id]
    similarity_points = product[user_row_id].flatten()
    user_similarity_points = list(zip(user_ids_ordered, similarity_points))
    all_similar_users = [x for x in user_similarity_points if x[1] > 0]

    user_reactions = pivot_table.iloc[user_row_id].to_numpy().flatten()
    similar_users_ids = [x[0] for x in all_similar_users]
    similar_users_rows_ids = [x for x in id_range if user_ids_ordered[x] in similar_users_ids]
    similar_users_reactions = pivot_table.iloc[similar_users_rows_ids].to_numpy()

    common_reactions = similar_users_reactions * user_reactions
    common_reactions_count = absolute(common_reactions).sum(axis=1)

    similarity_degree = [(all_similar_users[x][0], all_similar_users[x][1] / common_reactions_count[x]) for x in
                         range(len(common_reactions_count))]
    most_similar_users = sorted(similarity_degree, key=itemgetter(1), reverse=True)[:10]

    most_similar_users_ids = [x[0] for x in most_similar_users]
    return most_similar_users_ids


def get_recommendations(user_id: int, personal: bool = False):
    user_music = UserMusicIdSerializer(UserMusic.objects.filter(account_id=user_id), many=True).data
    user_music_ids = [x['recording_id'] for x in user_music]

    if personal:
        similar_users = get_similar_user_ids(user_id)
        if not similar_users:
            return []
        serializer = UserMusicRecommendationsSerializer(
            UserMusic.objects.filter(account_id__in=similar_users).exclude(like_status=0).exclude(
                recording_id__in=user_music_ids).values(), many=True)
    else:
        serializer = UserMusicRecommendationsSerializer(
            UserMusic.objects.all().exclude(like_status=0).exclude(recording_id__in=user_music_ids).values(), many=True)

    df = DataFrame.from_records(serializer.data)
    pivot_table = df.pivot_table(index='account_id', columns='recording_id', values='like_status', fill_value=0,
                                 dropna=True)
    aggregated_reactions = pivot_table.aggregate('sum') / len(pivot_table.index)
    aggregation_list = [x for x in zip(aggregated_reactions.keys(), aggregated_reactions.values) if x[1] > 0]
    recommendations = [x[0] for x in sorted(aggregation_list, key=itemgetter(1), reverse=True)][:30]
    return recommendations


def generate_recommendations(user_id: int):
    recommendations = get_recommendations(user_id, personal=True)
    if len(recommendations) < 30:
        recommendations.extend(
            [x for x in get_recommendations(user_id) if x not in recommendations][:30 - len(recommendations)])

    return recommendations
