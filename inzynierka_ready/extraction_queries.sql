/*---------------------------------------------------------------*/
/*					  DROP TABLES IF EXIST						 */
/*---------------------------------------------------------------*/

DROP TABLE IF EXISTS public.recording_dump;
DROP TABLE IF EXISTS public.artist_dump;
DROP TABLE IF EXISTS public.artist_inzynier_ready;
DROP TABLE IF EXISTS public.performed_dump;
DROP TABLE IF EXISTS public.recording_artist_dump;
DROP TABLE IF EXISTS public.recording_inzynier_ready;
DROP TABLE IF EXISTS public.performed_inzynier_ready;

/*---------------------------------------------------------------*/
/*					 CREATE TABLES FOR DUMP						 */
/*---------------------------------------------------------------*/

CREATE TABLE public.recording_dump (
	id bigserial NOT NULL,
	title varchar NOT NULL,
	length int,
	old_id bigint NOT NULL
);

CREATE TABLE public.artist_dump (
	id bigserial NOT NULL,
	stage_name varchar NOT NULL,
	old_id bigint NOT NULL
);

CREATE TABLE public.artist_inzynier_ready (
	id bigserial NOT NULL,
	stage_name varchar UNIQUE NOT NULL
);

CREATE TABLE public.performed_dump (
	recording_id bigint NOT NULL,
	artist_id bigint NOT NULL
);

CREATE TABLE public.recording_artist_dump (
	id bigserial NOT NULL,
	title varchar NOT NULL,
	length int,
	stage_name varchar NOT NULL
);

CREATE TABLE public.recording_inzynier_ready (
	id bigserial NOT NULL,
	title varchar NOT NULL,
	length int
);

CREATE TABLE public.performed_inzynier_ready (
	recording_id bigint NOT NULL,
	artist_id bigint NOT NULL
);

/*---------------------------------------------------------------*/
/*					  EXTRACT RELEVANT DATA						 */
/*---------------------------------------------------------------*/

-- Select artists chosen by community
INSERT INTO public.artist_dump(stage_name, old_id)
	SELECT stage_name, id
	FROM public.musicly_artist
	WHERE lower(stage_name) IN ('dawid podsiadło', 'metallica', 'u2', 'maroon 5', 'sarsa', 'viki gabor', 'sanah', 'paktofonika', 'mata', 'trzeci wymiar', 'jamal', 'grubson', 'ich troje', 'doda', 'idina menzel', 'zendaya', 'taylor swift', 'conan grey', 'thefatrat', 'alan walker', 'avicii', 'alvaro soler', 'luis fonsi', 'indila', 'avril lavigne', 'selena gomez', 'demi lovato', 'harry styles', 'łydka grubasa', 'łąki łan', 'bracia figo fagot', 'red hot chilli peppers', 'nirvana', 'coldplay', 'imagine dragons', 'queen', 'fokus', 'rahim', 'o.s.t.r', 'dwa sławy', 'happysad', 'levis capaldi', 'ed sheeran', 'bon jovi', 'rick astley', 'kwiat jabłoni', 'daria zawiałow', 'kortez', 'maryla rodowicz', 'julia pośnik', 'shakira', 'rihanna', 'beyonce', 'eminem', 'drake', 'kygo', 'keane', 'young leosia', 'alphaville', 'gorillaz', 'kongos', 'toto', 'tessa violet', 'sia', 'c-bool', 'sara bareilles', 'marie', 'the weekend', 'shawn mendes', 'marshmello', 'anne reburn', 'billie eilish', 'dua lipa', 'katy perry', 'blackbear', 'aitana', 'lenka', 'astrid s', 'carly rae jepsen', '5 seconds of summer', 'system of a down', 'męskie granie', 'quebonafide', 'taco hemingway', 'pharrell williams', 'lost frequencies', 'regina spektor', 'adam lambert', 'ingrid michaelson', 'arctic monkeys', 'eldo', 'ariana grande', 'dolly parton', 'p!nk', 'lady pank', 'dżem', 'jonas brothers', 'one direction', 'michael jackson', 'elvis presley', 'tokio hotel', 'justin bieber', 'enrique iglesias', 'wojtek szumański', 'mint', 'the lumineers', 'elton john', 'linkin park', 'green day', 'led zeppelin', 'poparzeni kawą trzy', 'koniec świata', 'nf', 'twenty one pilots', 'zenek martyniuk', 'bad omens', 'kings of leon', 'ac/dc', 'wilki', 'papa roach', 'jay-z', 'paramore', 'foo fighters', 'sobel', 'ostr', 'bedoes', 'ralph kaminski', 'miuosh', 'grace vanderwaal', 'grzegorz hyży', 'the beatles', 'sabaton', 'the piano guys', 'tycho', 'slayer', 'black sabbath', 'ozzy osbourne', 'motorhead', 'behemoth', 'iron maiden', 'manowar', 'king diamond', 'nocny kochanek', 'one republic', 'enej', 'elektryczne gitary', 'trubadurzy', 'tercet egzotyczny', 'lady gaga', 'white lies', 'the weeknd', 'the black mamba', 'abba', 'rita ora', 'michał szczygieł', 'malik montana', 'kizo', 'krzysztof krawczyk', 'kali', 'bracia golec', 'roksana węgiel', 'madonna', 'vito bambino', 'the xx', 'krzysztof zalewski', 'tame impala', 'atlvnta', 'brodka', 'aurora', 'bitamina', 'guzior', 'pro8l3m', 'paluch', 'muse', 'queens of the stone age', 'bon iver', 'bahamas', 'sam smith', 'nick leng', 'fletcher', 'lorde', 'clairo', 'david gilmour', 'wilco', 'big red machine', 'wallows', 'mild orange', 'pink floyd', 'neighbourhood', 'florence and the machine', '21 pilots', 'enter', 'tymek', 'margaret', 'rodriguez', 'van morrison', 'ben king', 'simon&garfunkel', 'bon dylan', 'fleetwood mac', 'the beach boys', 'perfect', 'czerwone gitary', 'golec uorkiestra', 'boys', 'akcent', 'bring me the horizon', 'miley cyrus', 'dermot kennedy', 'anne-marie', 'olivia addams', 'post malone', 'lil peep', 'wiz khalifa', 'tede', 'reto', 'rammstein', 'kękę', 'pawbeats', 'sokół', 'king of leons', 'oberschleisen', 'strachy na lachy', 'audioslave', 'kiss', 'van halen', 'the proclaimers', 'łzy', 'republika', 'zeus', 'szpaku', 'peja', 'kaen', 'verba', 'mig', 'weekend', 'piękni i młodzi', 'milky chance', 'peach pit', 'meek oh why', 'wilkinson', 'the dumplings', 'pezet', 'uknown mortal otchestra', 'coma', 'budka suflera', 'luxtorpeda', 'sarius', 'birdy', 'john mayer', 'organek', 'john legend', 'tom odell', 'o.s.t.r.', 'hunter', 'myslovitz', 'tenacious d', 'słoń', 'the offspring', 'cleo', 'dotan', 'ava max', 'martin garix', 'ona', 'agnieszka chylińska', 'him', 'korn', 'modern talking', 'zbigniew wodecki', 'bennasi bross', 'dj kris', 'dj matys', 'paul kalkbrennen', 'boris brejcha', 'digital rockers', 'sonbird', 'cher', 'a-ha', 'leonard cohen', 'marek grechuta', 'tanita tikaram', 'roxette', 'sting', 'hollywood undead', 'skillet', 's0cliché', 'italobrothers', 'the kid laroi', 'three days grace', 'thousand foot krutch', 'five finger death punch', 'the cat empire', 'rhye', 'breakout', 'dave matthews band', 'sdm', 'pidżama porno', 'spice girls', 'backstreet boys', 'kombi', 'chłopcy z placu broni', 'lemon', 'radiohead', 'hey', 'royal blood', 'royal deluxe', 'dorothy', 'greta van fleet', 'grandson', 'des rocs', 'barns courtney', 'tuzza', 'pikers', 'juice wrld', 'chief keef', 'lil uzi vert', 'yung lean', 'xxxtentacion', 'bladee', 'lil baby', 'panic at the disco', 'camilla cabello', 'varius manx', 'krzysztof cugowski', 'bracia', 'zakopower', 'blue cafe', 'pectus', 'de mono', 'alexander rybak', 'adele', 'the jacksons', 'wham!', 'electric light orchestra', 'village people', 'backstreets boys', 'earth wind & fire', 'redbone', 'wild cherry', 'the hu', 'pearl jam', 'beatles', 'sex pistols', 'the rolling stones', 'the band', 'bad company', 'tiesto', 'stachurski', 'edyta górniak', 'michał szpak', 'the strokes', 'darkside', 'dorian electra', 'alestorm', 'jamie woon', 'sevdaliza', 'kraftwerk', 'the paper knites', 'nickelback', 'doris day', 'of monster and man', 'disturbed', 'frank sinatra', 'creed', 'etta jones', 'g-eazy', 'żabson', 'kuban', 'kaz bałagane', 'travis scott', 'kukon', 'sentino', 'rhcp', 'rolling stones', 'counting crows', 'john elton', 'eric clapton', 'amy winehouse', 'nina simone', 'aretha franklin', 'louis armstrong', 'katie melua', 'artur rojek', 'fka twigs', 'depeche mode', 'lana del rey', 'lenny kravitz', 'sarah', 'l.stadt', 'jackson', 'sandra', 'kult', 'ezra', 'ryczące 20', 'lipnicka', 'bajm', 'cnco', 'kylie minogue', 'jon bellion', 'kayah', 'patrycja markowska', 'little mix', 'x ambassadors', 'the killers', 'hozier', 'whitney houston', 'skaldowie', 'the doors', 'the chainsmokers', 'jax jones', 'lil nas x', 'smokie', 'james bay', 'justin timberlake', 'andrea bocelli', 'il volo', 'jan kondrak', 'marek andrzejewski', 'lubelska federacja bardów', 'wolna grupa bukowina', 'piotr bakal', 'cztery pory miłowania', 'leonard luther', 'czerwony tulipan', 'jose torres', 'leszek możdżer', 'sylwia grzeszczak', 'sławomir', 'gracjan roztocki', 'dub fx', 'st mungo hi fi', 'balkan beat box', 'seun kuti', 'tinariven', 'peatbog feries', 'bjork', 'kabanos', 'dr alban', 'kaleo', 'leon bridges', 'two feet', 'disclosure', 'alt-j', 'hannah montana', 'timbaland', 'ghost', 'bbno$', 'powerwolf', 'miracle of sound', 'marylin manson', 'prometh', 'bee gees', 'ania wyszkoni', 'prince', 'bisz', 'rasmentalism', 'nightwish', 'dire straits', 'nothing but thieves', 'mrozu', 'sam fender', 'enter shikari', 'podsiadło', 'kaminski', 'zalewski', 'domagała', 'górniak', 'rynkowski', 'lady punk', 'big cyc', 'bracia cugowscy', 'feel', 'monika brodka', 'lentra / the ceo of business', 'zztop', 'young gravy', 'maneskin', 'xandria', 'dawid bowie', 'lmc', 'miyavi', 'nujabes', 'childish gambino', 'asgeir', 'bass astral x igo', 'chet faker', 'bruno mars', 'bieberjustin timberlake', 'nicki minaj', 'białas', 'natalia szroeder', 'ewa farna', 'aerosmith', 'greensky bluegrass', 'miętha', 'slipknot', 'genesis', 'michael kiwanuka', 'manu chao', 'chemical brothers', 'massive attack', 'agnes obel', 'moloko', 'grimes', 'blackpink', 'maria peszek', 'iggy azalea', 'britney spears', 'limp bizkit', 'fall out boy', 'the prodigy', 'the black eyed peas', 'król', 'the florence and the machine', 'oxon', 'łona', 'karolcia', 'mela koteluk', 'dawid kwiatkowski', '30 seconds to mars', 'beast in black', 'the neighbourhood', 'pet shop boys', 'fancy', 'phil collins', 'earth', 'wind & fire', 'andrzej piaseczny', 'ira', 'edyta bartosiewicz', 'opał', 'gibbs', 'zbuku', 'kartky', 'oio', 'eivor', 'wardruna', 'forest swords', 'klangkarussell', 'victoria', 'sel', 'wiktor coj', 'sisters on wire', 'hande yenner', 'artic monkeys', 'anna maria jopek', 'projekt laureaci', 'ekt gdynia', 'mechanicy szanty', 'stare dzwony', 'michał bajor', 'grechuta', 'anawa', 'trzecia miłość', 'perły i łotry', 'merghani', 'young multi', 'doja cat', 'def leppard', 'paradise lost', 'judas priest', 'oreada', 'caryna', 'łysa góra', 'sztywny pal azji', 'power of trinity', 'evanescence', 'bez jacka', 'epica', 'tower of power', 'wulfpeck', 'stevie wonder', 'jungle', 'quantic', 'marillion', 'bryan adams', 'carrion', 'janusz radek', 'dr misio', 'scorpions', 'poets of the fall', 'asap rocky', 'tupac', 'snoop dog', 'lizo', 'álvaro soler', 'maluma', 'parkway drive', 'rammstain', 'indios bravos', 'don vasyl', 'mikromusic', 'paweł domagała', 'sławek uniatowski', 'the wreckage', 'the rasmus', 'eluveitie', 'korpiklaani', 'in this moment', 'pendulum', 'bruklin', 'piotr rogucki', 'halsey', 'bmth', 'kuba badach', 'mietek szcześniak', 'deep purple', 'lech janerka', 'bez idola', 'grzegorz turnau', 'george michael', 'peter gabriel', 'mesajah', 'zuza jabłońska', 'robert plant', 'logic', 'partyboi69', 'tash sultana', 'beirut', 'jacek stachursky', 'młody dzban', 'david guetta', 'quadriga consort', 'jethro tull', 'apocalyptica', 'snow patrol', 'danil trifonov', 'jan lisiecki', 'luigi tenco', 'the choral scholars', 'julie fowlis', 'the fray', 'dominik wagner', 'mikyung sung', 'scott mulvahill', 'lucio battisti', 'gypsy kings', 'hill song', 'nie ma go tu', 'polish violino duo', 'fundacja incanto etc', 'one ok rock', 'bridgit mendler')
	ORDER BY id;

-- Select distinct artist names
INSERT INTO public.artist_inzynier_ready(stage_name)
	SELECT DISTINCT stage_name
	FROM public.artist_dump;

-- Select all performances of the chosen artists
INSERT INTO public.performed_dump(recording_id, artist_id)
	SELECT recording_id, artist_id
	FROM public.musicly_performed
	JOIN public.artist_dump ON (musicly_performed.artist_id = artist_dump.id);

-- Select all recordings of all chosen artists
INSERT INTO public.recording_dump(title, length, old_id)
	SELECT title, length, id
	FROM public.musicly_recording
	JOIN public.performed_dump ON (musicly_recording.id = performed_dump.recording_id)
	ORDER BY id;

-- Merge recordings with their artists into one table for simplicity
INSERT INTO public.recording_artist_dump(title, length, stage_name)
	SELECT title,
		(SELECT length
			FROM public.recording_dump
				JOIN public.performed_dump ON (recording_dump.id = performed_dump.recording_id)
				JOIN public.artist_dump ON (artist_dump.id = performed_dump.artist_id)
			WHERE stage_name = ad.stage_name
			AND title = rd.title
			AND length IS NOT NULL
			ORDER BY length
			LIMIT 1),
		stage_name
	FROM public.recording_dump rd
		JOIN public.performed_dump pd ON rd.id = pd.recording_id
		JOIN public.artist_dump ad ON pd.artist_id = ad.id
	GROUP BY stage_name, title;

-- Extract recording list from ^that blob
INSERT INTO public.recording_inzynier_ready(title, length)
	SELECT title, length
	FROM public.recording_artist_dump
	ORDER BY id;

-- Extract performance info from ^that table and ^^that blob
INSERT INTO public.performed_inzynier_ready(recording_id, artist_id)
	SELECT rir.id, air.id
	FROM public.recording_inzynier_ready rir
		JOIN recording_artist_dump rad ON (rir.id = rad.id)
		JOIN public.artist_inzynier_ready air ON (air.stage_name = rad.stage_name);

/*---------------------------------------------------------------*/
/*					  CLEAN AFTER YOURSELF						 */
/*---------------------------------------------------------------*/

DROP TABLE IF EXISTS public.recording_dump;
DROP TABLE IF EXISTS public.artist_dump;
DROP TABLE IF EXISTS public.performed_dump;
DROP TABLE IF EXISTS public.recording_artist_dump;

/*---------------------------------------------------------------*/
