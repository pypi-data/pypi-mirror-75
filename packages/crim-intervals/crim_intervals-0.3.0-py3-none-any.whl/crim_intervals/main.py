from music21 import *
import music21 as m21
import time
import requests
from pathlib import Path

# An extension of the music21 note class with more information easily accessible
class NoteListElement:
    """
    An extension of the music21 note class

    Attributes
    ----------
    note : m21.note.Note
        music21 note class
    offset : int
        cumulative offset of note
    id : int
        unique music21 id
    metadata : music21.metadata
        piece metadata- not normally attached to a music21 note
    part : str
        voice name
    partNumber : int
        voice number, not 0 indexed
    duration : int
        note duration
    piece_url : str
        piece url for note
    """
    def __init__(self, note: m21.note.Note, metadata, part, partNumber, duration, piece_url):
        self.note = note
        self.offset = self.note.offset
        self.id = self.note.id
        self.metadata = metadata
        self.part = part
        self.partNumber = partNumber
        self.duration = duration
        self.piece_url = piece_url

    def __str__(self):
        return "<NoteListElement: {}>".format(self.note.name)

# For mass file uploads, only compatible for whole piece analysis, more specific tuning to come
class CorpusBase:
    # Need to consider whether users can input certain scores (which means needing urls selected too), or just to do all in the corpus automatically
    """
    A class for importing multiple scores at once

    Attributes
    ----------
    urls : list
        list of urls of scores to be imported
    paths : list
        list of file paths of scores to be imported
    scores : list of music21.Score
        list of music21.Score objects- imported from urls and paths
    all_urls : list
        stores both paths and urls- not for user usage
    note_list : list of NoteListElement
        list of notes constructed from scores
    note_list_no_unisons : list of NoteListElement
        list of notes constructed from scores, combining unisons
    """
    def __init__(self, urls:list, paths:list):
        """
        Parameters
        ----------
        urls : list
            list urls to mei files
        paths : list
            list paths to mei files

        Raises
        ----------
        Exception
            If at least one score isn't succesfully imported, raises error
        """
        self.urls = urls
        self.paths = paths
        self.scores = []
        self.all_urls = []
        for url in urls:
            print("Requesting file from " + str(url) + "...")
            try:
                self.scores.append(m21.converter.parse(requests.get(url).text))
                print("Successfully imported.")
                self.all_urls.append(url)
            except:
                print("Import from " + str(url) + " failed, please check your url/file type. Continuing to next file...")
        mei_conv = converter.subConverters.ConverterMEI()
        for path in paths:
            print("Requesting file from " + str(path) + "...")
            try:
                self.scores.append(mei_conv.parseFile(path))
                print("Successfully imported.")
                self.all_urls.append(path)
            except:
                print("Import of " + str(path) + " failed, please check your file path/file type. Continuing to next file...")
        if len(self.scores) == 0:
            raise Exception("At least one score must be succesfully imported")
        self.note_list = self.note_list_whole_piece()
        self.no_unisons = self.note_list_no_unisons()

    def note_list_whole_piece(self):
        """ Creates a note list from the whole piece for all scores- default note_list
        """
        pure_notes = []
        urls_index = 0
        for score in self.scores:
            parts = score.getElementsByClass(stream.Part)
            for part in parts:
                noteList = part.flat.getElementsByClass(['Note', 'Rest'])
                for note in noteList:
                    if note.tie is not None:
                        if note.tie.type == 'start':
                            note_obj = NoteListElement(note, score.metadata, part.partName, score.index(part), note.quarterLength, self.all_urls[urls_index])
                            pure_notes.append(note_obj)
                        else:
                            pure_notes[len(pure_notes)-1].duration += note.quarterLength
                    else:
                        note_obj = NoteListElement(note, score.metadata, part.partName, score.index(part), note.quarterLength, self.all_urls[urls_index])
                        pure_notes.append(note_obj)
                note_obj = NoteListElement(m21.note.Rest(), score.metadata, part.partName, score.index(part), 4.0, self.all_urls[urls_index])
                pure_notes.append(note_obj)
            urls_index += 1
        return pure_notes

    def note_list_no_unisons(self):
        """ Creates a note list from the whole piece for all scores combining unisons

        Combines consecutive notes at the same pitch into one note, adding in the duration
        of the next note into the previous one.
        """
        pure_notes = []
        urls_index = 0
        for score in self.scores:
            parts = score.getElementsByClass(stream.Part)
            for part in parts:
                noteList = part.flat.getElementsByClass(['Note', 'Rest'])
                prev_pitch = None
                for note in noteList:
                    if not note.isRest and note.nameWithOctave == prev_pitch:
                        pure_notes[len(pure_notes)-1].duration += note.quarterLength
                    else:
                        note_obj = NoteListElement(note, score.metadata, part.partName, score.index(part), note.quarterLength, self.all_urls[urls_index])
                        pure_notes.append(note_obj)
                    if not note.isRest:
                        prev_pitch = note.nameWithOctave
                    else:
                        prev_pitch == 'Rest'
                note_obj = NoteListElement(m21.note.Rest(), score.metadata, part.partName, score.index(part), 4.0, self.all_urls[urls_index])
                pure_notes.append(note_obj)
            urls_index += 1
        return pure_notes

    def note_list_selected_offset(self, offsets: list):
        """
        Creates a note list from the whole piece for all scores, going by provided offsets

        Parameters
        ----------
        offsets : list
            offsets within measures to collect notes at (notes collected will be those that are sounding at that offset- not just starting)
        """
        pure_notes = []
        urls_index = 0
        for score in self.scores:
            parts = score.getElementsByClass(stream.Part)
            for part in parts:
                measures = part.getElementsByClass(stream.Measure)
                for measure in measures:
                    voices = measure.getElementsByClass(stream.Voice)
                    for voice in voices:
                        for note in voice:
                            for point in offsets:
                                #print(note.offset, point)
                                if point >= note.offset and point < (note.offset + note.quarterLength):
                                    note_obj = NoteListElement(note, score.metadata, part.partName, score.index(part), note.quarterLength, self.all_urls[urls_index])
                                    pure_notes.append(note_obj)
                                    break
            urls_index += 1
        return pure_notes

# For single file uploads
class ScoreBase:
    """
    A class for importing a single score- offers more precise construction options

    Attributes
    ----------
    url : str
        url or path of mei file
    score : music21.Score
        music21.Score object gathered from mei file import
    note_list : list of NoteListElement
        list of notes constructed from score
    """
    def __init__(self, url):
        """
        Parameters
        ----------
        url:
            url or path of mei file
        Raises
        ----------
        Exception
            If score isn't succesfully imported, raises error
        """
        self.url = url
        print("Requesting file from " + str(self.url) + "...")
        # Detect if local file of url based on leading /
        if url[0] == '/':
            try:
                self.score = converter.subConverters.ConverterMEI().parseFile(url)
                print("Successfully imported.")
            except:
                raise Exception("Import from " + str(self.url) + " failed, please check your ath/file type")
        else:
            try:
                self.score = m21.converter.parse(requests.get(self.url).text)
                print("Successfully imported.")
            except:
                raise Exception("Import from " + str(self.url) + " failed, please check your url/file type")
        self.note_list = self.note_list_whole_piece()

    def note_list_whole_piece(self):
        """ Creates a note list from the whole piece- default note_list
        """
        pure_notes = []
        parts = self.score.getElementsByClass(stream.Part)
        for part in parts:
            noteList = part.flat.getElementsByClass(['Note', 'Rest'])
            for note in noteList:
                if note.tie is not None:
                    if note.tie.type == 'start':
                        note_obj = NoteListElement(note, self.score.metadata, part.partName, self.score.index(part), note.quarterLength, self.url)
                        pure_notes.append(note_obj)
                    else:
                        pure_notes[len(pure_notes)-1].duration += note.quarterLength
                else:
                    note_obj = NoteListElement(note, self.score.metadata, part.partName, self.score.index(part), note.quarterLength, self.url)
                    pure_notes.append(note_obj)
            note_obj = NoteListElement(m21.note.Rest(), self.score.metadata, part.partName, self.score.index(part), 4.0, self.url)
            pure_notes.append(note_obj)
        return pure_notes

    # Combines unison intervals into one note- generally for increased pattern finding
    def note_list_no_unisons(self):
        """ Creates a note list from the whole piece for all scores combining unisons

        Combines consecutive notes at the same pitch into one note, adding in the duration
        of the next note into the previous one.
        """
        pure_notes = []
        urls_index = 0
        parts = self.score.getElementsByClass(stream.Part)
        for part in parts:
            noteList = part.flat.getElementsByClass(['Note', 'Rest'])
            prev_pitch = None
            for note in noteList:
                if not note.isRest and note.nameWithOctave == prev_pitch:
                    pure_notes[len(pure_notes)-1].duration += note.quarterLength
                else:
                    note_obj = NoteListElement(note, self.score.metadata, part.partName, self.score.index(part), note.quarterLength, all_urls[urls_index])
                    pure_notes.append(note_obj)
                if not note.isRest:
                    prev_pitch = note.nameWithOctave
                else:
                    prev_pitch == 'Rest'
            note_obj = NoteListElement(m21.note.Rest(), self.score.metadata, part.partName, self.score.index(part), 4.0, all_urls[urls_index])
            pure_notes.append(note_obj)
        urls_index += 1
        return pure_notes

    # Gets only notes that start on the specified beats- allows for user specification in case of weird time signatures
    def note_list_selected_beats(self, beats: list):
        """
        Creates a note list from the whole piece, going by provided beats

        Parameters
        ----------
        beats : list
            collects all notes which begin on specified beat
        """
        pure_notes = []
        parts = self.score.getElementsByClass(stream.Part)
        for part in parts:
            noteList = part.flat.getElementsByClass(['Note', 'Rest'])
            for note in noteList:
                if note.beat in beats:
                        note_obj = NoteListElement(note, self.score.metadata, part.partName, self.score.index(part), note.quarterLength, self.url)
                        pure_notes.append(note_obj)
            note_obj = NoteListElement(m21.note.Rest(), self.score.metadata, part.partName, self.score.index(part), 4.0, self.url)
            pure_notes.append(note_obj)
        return pure_notes

    def note_list_by_offset(self, offsets:list):
        """
        Creates a note list from the whole piece, going by provided offsets

        Parameters
        ----------
        offsets : list
            offsets within measures to collect notes at (notes collected will be those that are sounding at that offset- not just starting)
        """
        pure_notes = []
        part_number = 0
        parts = self.score.getElementsByClass(stream.Part)
        for part in parts:
            part_number += 1
            measures = part.getElementsByClass(stream.Measure)
            for measure in measures:
                voices = measure.getElementsByClass(stream.Voice)
                for voice in voices:
                    for note in voice:
                        for point in offsets:
                            if point >= note.offset and point < (note.offset + note.quarterLength):
                                note_obj = NoteListElement(note, self.score.metadata, part.partName, part_number, note.quarterLength, self.url)
                                pure_notes.append(note_obj)
                                break
        return pure_notes

    # Allows for very specific note selection
    def note_list_single_part(self, part, measure_start, num_measures):
        """
        Creates a note list from a selected measure range within a single voice

        Parameters
        ----------
        part : int
            part number
        measure_start : int
            starting measure
        num_measures : int
            measures until end measure
        """
        pure_notes = []
        part_selected = self.score.getElementsByClass(stream.Part)[part]
        measures = part_selected.getElementsByClass(stream.Measure)
        measures_selected = []
        for i in range(num_measures):
            measures_selected.append(measures[i+measure_start])
        for measure in measures_selected:
            voices = measure.getElementsByClass(stream.Voice)
            for voice in voices:
                for note in voice:
                    print(note.offset)
                    if note.tie is not None:
                        if note.tie.type == 'start':
                            note_obj = NoteListElement(note, self.score.metadata, part_selected.partName, part, note.quarterLength, self.url)
                            pure_notes.append(note_obj)
                        else:
                            pure_notes[len(pure_notes)-1].duration += note.quarterLength
                    else:
                        note_obj = NoteListElement(note, self.score.metadata, part_selected.partName, part, note.quarterLength, self.url)
                        pure_notes.append(note_obj)
        return pure_notes

    # Allows for specific selection in terms of measures, but gets all parts/instruments
    def note_list_all_parts(self, measure_start, num_measures):
        """
        Creates a note list from a selected measure range over all voices

        Parameters
        ----------
        measure_start : int
            starting measure
        num_measures : int
            measures until end measure
        """
        pure_notes = []
        parts = self.score.getElementsByClass(stream.Part)
        for part in parts:
            measures = part.getElementsByClass(stream.Measure)
            measures_selected = []
            for i in range(num_measures):
                measures_selected.append(measures[i+measure_start])
            for measure in measures_selected:
                voices = measure.getElementsByClass(stream.Voice)
                for voice in voices:
                    for note in voice:
                        if note.tie is not None:
                            if note.tie.type == 'start':
                                note_obj = NoteListElement(note, self.score.metadata, part.partName, self.score.index(part), note.quarterLength, self.url)
                                pure_notes.append(note_obj)
                            else:
                                pure_notes[len(pure_notes)-1].duration += note.quarterLength
                        else:
                            note_obj = NoteListElement(note, self.score.metadata, part.partName, self.score.index(part), note.quarterLength, self.url)
                            pure_notes.append(note_obj)
            # Added rest to ensure parts don't overlap
            note_obj = NoteListElement(m21.note.Rest(), self.score.metadata, part.partName, self.score.index(part), 4.0, self.url)
            pure_notes.append(note_obj)
        return pure_notes


class VectorInterval:
    """
    An individual vector with information about the notes creating it

    Attributes
    ----------
    vector : int or str
        vector- in generic or semitones: is "Rest" if done between a note and a rest
    note1 : NoteListElement
        first note of interval pair
    note2 : NoteListElement
        list of notes constructed from score
    """
    def __init__(self, vector, note1: NoteListElement, note2: NoteListElement):
        self.vector = vector
        self.note1 = note1
        self.note2 = note2

    def __str__(self):
        if self.note1.note.isRest or self.note2.note.isRest:
            return "<VectorInterval: Rest, First Note: {}, Second Note: {}>".format(self.vector, self.note1.note, self.note2.note)
        else:
            return "<VectorInterval: {}, First Note: {}, Second Note: {}>".format(self.vector, self.note1.note.nameWithOctave, self.note2.note.nameWithOctave)

# Allows for selected "vectorizations" given a note list created from either ScoreBase or CorpusBase
# Consider making this a Standalone method- an object seems slightly redundant/hard to justify
class IntervalBase:
    """
    A list of VectorInterval objects created from a note list

    Attributes
    ----------
    notes : list
        note list gathered from either CorpusBase or ScoreBase's methods/attributes
    generic_intervals : list
        creates list of VectorInterval objects in terms of generic intervals
    semitone_intervals : list
        creates list of VectorInterval objects in terms of semitone intervals
    """
    def __init__(self, notes):
        """
        Parameters
        ----------
        notes:
            note list gathered from either CorpusBase or ScoreBase's methods/attributes
        """
        self.notes = notes
        self.generic_intervals = self.vectorize_generic(self.notes)
        self.semitone_intervals = self.vectorize_semitone(self.notes)

    # Construct intervals in terms of semitone distances between notes
    def vectorize_semitone(self, notes):
        """Creates list of VectorInterval objects in terms of semitone intervals

        Parameters
        ----------
        notes:
            (frequently self.notes): note list gathered from either CorpusBase or ScoreBase's methods/attributes
        """
        vec = []
        for i in range(len(notes)-1):
            if notes[i].note.isRest or notes[i+1].note.isRest:
                interval_obj = VectorInterval("Rest", notes[i], notes[i+1])
                vec.append(interval_obj)
            else:
                interval_semitones = interval.Interval(notes[i].note, notes[i+1].note).semitones
                interval_obj = VectorInterval(interval_semitones, notes[i], notes[i+1])
                vec.append(interval_obj)
        return vec

    # Construct intervals in terms of generic distance between notes
    def vectorize_generic(self, notes):
        """Creates list of VectorInterval objects in terms of generic intervals

        Parameters
        ----------
        notes:
            (frequently self.notes): note list gathered from either CorpusBase or ScoreBase's methods/attributes
        """
        vec = []
        for i in range(len(notes)-1):
            if notes[i].note.isRest or notes[i+1].note.isRest:
                interval_obj = VectorInterval("Rest", notes[i], notes[i+1])
                vec.append(interval_obj)
            else:
                interval_semitones = interval.Interval(notes[i].note, notes[i+1].note).semitones
                interval_obj = VectorInterval(interval.convertSemitoneToSpecifierGeneric(interval_semitones)[1], notes[i], notes[i+1])
                vec.append(interval_obj)
        return vec

# An individual match event- can be used for close matches as well
class Match:
    """
    A pattern that has been deemed part of a match

    Attributes
    ----------
    pattern : list
        list of vectors in pattern
    first_note : NoteListElement
        first note in the soggetti creating the vector pattern
    last_note : NoteListElement
        last note in the soggetti creating the vector pattern
    durations : list
        list of durations of notes in soggetti creating the vector pattern
    ema : str
        standalone ema snippet for the pattern
    ema_url : str
        url to get mei for the pattern
    """
    def __init__(self, pattern, first_note: NoteListElement, last_note: NoteListElement, durations):
        self.pattern = pattern
        self.first_note = first_note
        self.last_note = last_note
        # Construct an ema address for the entire pattern to pass on
        ema =  str(self.first_note.note.measureNumber) + "-" + str(self.last_note.note.measureNumber) + "/" + str(self.first_note.partNumber) + "/"
        ema += ("@" + str(self.first_note.note.beat) + "-end")
        for i in range(self.last_note.note.measureNumber - self.first_note.note.measureNumber - 1):
            ema += ",@start-end"
        ema += (",@start-" + str(self.last_note.note.beat))
        self.ema = ema
        try:
            splice = self.first_note.piece_url.index('mei/')
            self.ema_url = "https://ema.crimproject.org/https%3A%2F%2Fcrimproject.org%2Fmei%2F" + str(self.first_note.piece_url[splice + 4:]) + "/" + str(self.ema)
        except:
            self.ema_url = "File must be a crim url to have a valid EMA url"
        self.durations = durations

# Object representing all the occurences of a pattern in a list of notes/vectors
# User generally doesn't create this- it is done in the finding matches methods
class PatternMatches:
    """
    A group of Match objects generated from a pattern

    Attributes
    ----------
    pattern : list
        pattern generating matches
    matches : list
        list of Match objects found to be matching the pattern
    """
    def __init__(self, pattern, matches:list):
        self.pattern = pattern
        self.matches = matches

    def print_exact_matches(self):
        """A facilitated way to display all the matches gathered by a find_exact_matches search
        """
        print("Melodic interval/pattern " + str(self.pattern) + " occurs " + str(len(self.matches)) + " times:")
        for match in self.matches:
            print("In " + str(match.first_note.metadata.title) + " part " + str(match.first_note.part) + " beginning in measure " + str(match.first_note.note.measureNumber) +\
            " and ending in measure " + str(match.last_note.note.measureNumber) + ". Notes lengths: " + str(match.durations))
        print("\n")

    def print_close_matches(self):
        """A facilitated way to display all the matches gathered by a find_close_matches search
        """
        print("Occurences of " + str(self.pattern) + " or similar:")
        for match in self.matches:
            print("Pattern " + str(match.pattern) + " appears in " + str(match.first_note.metadata.title) + " part " + str(match.first_note.part) + " beginning in measure " + str(match.first_note.note.measureNumber) +\
            " and ending in measure " + str(match.last_note.note.measureNumber) + ". Notes lengths: " + str(match.durations))
        print("Said pattern or similar appeared " + str(len(self.matches)) + " times.\n")

# Potential redesign needed due to unstable nature of having user give over patterns_data
# Potential fix is reincorporating into_patterns back into this method
def find_exact_matches(patterns_data, min_matches=5):
    """Takes in a series of vector patterns with data attached and finds exact matches

    Parameters
    ----------
    patterns_data : return value from into_patterns
        MUST be return value from into_patterns
    min_matches : int, optional
        Minimum number of matches needed to be deemed relevant, defaults to 5

    Returns
    -------
    all_matches_list : list
        A list of PatternMatches objects
    """
    # A series of arrays are needed to keep track of various data associated with each pattern
    print("Finding exact matches...")
    patterns_nodup, patterns = [], []
    p = 0
    for pattern in patterns_data:
        patterns.append(pattern[0])
        if pattern[0] not in patterns_nodup:
            patterns_nodup.append(pattern[0])
    m = 0
    # Go through each individual pattern and count up its occurences
    all_matches_list = []
    for p in patterns_nodup:
        amt = patterns.count(p)
        # If a pattern occurs more than the designated threshold, we add it to our list of matches
        if amt > min_matches:
            matches_list = PatternMatches(p, [])
            m += 1
            for a in patterns_data:
                if p == a[0]:
                    exact_match = Match(p, a[1], a[2], a[3])
                    matches_list.matches.append(exact_match)
            all_matches_list.append(matches_list)
    print(str(len(all_matches_list)) + " melodic intervals had more than " + str(min_matches) + " exact matches.\n")
    # all_matches_list has a nested structure- it contains a list of PatternMatches objects, which contain a list of individual Match objects
    return all_matches_list

# Finds matches based on a cumulative distance difference between two patterns
def find_close_matches(patterns_data, min_matches, threshold):
    """Takes in a series of vector patterns with data attached and finds close matches

    Parameters
    ----------
    patterns_data : return value from into_patterns
        MUST be return value from into_patterns
    min_matches : int, optional
        Minimum number of matches needed to be deemed relevant, defaults to 5
    threshold : int
        Cumulative variance allowed between vector patterns before they are deemed not similar

    Returns
    -------
    all_matches_list : list
        A list of PatternMatches objects
    """
    # A series of arrays are needed to keep track of various data associated with each pattern
    print("Finding close matches...")
    patterns_nodup = []
    for pat in patterns_data:
        # Build up a list of patterns without duplicates
        if pat[0] not in patterns_nodup:
            patterns_nodup.append(pat[0])
    # Go through each individual pattern and count up its occurences
    all_matches_list = []
    for p in patterns_nodup:
        matches_list = PatternMatches(p, [])
        # If a pattern occurs more than the designated threshold
        for a in patterns_data:
            match = 0
            # Calculate the "difference" by comparing each vector with the matching on in the other pattern
            for v in range(len(a[0])):
                match += abs(p[v] - a[0][v])
            if match <= threshold:
                close_match = Match(a[0], a[1], a[2], a[3])
                matches_list.matches.append(close_match)
        if len(matches_list.matches) > min_matches:
            all_matches_list.append(matches_list)
    print(str(len(all_matches_list)) + " melodic intervals had more than " + str(min_matches) + " exact or close matches.\n")
    return all_matches_list

# Allows for the addition of non-moving-window pattern searching approaches
# Needs to be called before any matches can be made
def into_patterns(vectors_list, interval):
    """Takes in a series of vector patterns with data attached and finds close matches

    Parameters
    ----------
    vectors_list : list of vectorized lists
        MUST be a list from calling generic_intervals or semitone_intervals on a VectorInterval object
    interval : int
        size of interval to be analyzed

    Returns
    -------
    patterns_data : list of tuples
        A list of vector patterns with additional information about notes attached
    """
    pattern, patterns_data = [], []
    for vectors in vectors_list:
        for i in range(len(vectors)-interval):
            pattern = []
            durations = []
            valid_pattern = True
            durations.append(vectors[i].note1.duration)
            for num_notes in range(interval):
                if vectors[i+num_notes].vector == 'Rest':
                    valid_pattern = False
                pattern.append(vectors[i+num_notes].vector)
                durations.append(vectors[i+num_notes].note2.duration)
            if valid_pattern:
            # Here, with help from vectorize() you can jam in whatever more data you would like about the note
                patterns_data.append((pattern, vectors[i].note1, vectors[i+num_notes].note2, durations))
    return patterns_data

# Helper for sort_matches
def sortFunc(pattern):
    """Helper function for sort_matches
    """
    return len(pattern.matches)

# Sorting based on the amount of matches each pattern has
def sort_matches(matches_list):
    """Sorts and returns a list of PatternMatch objects, ordering by size
    """
    matches_list.sort(reverse=True, key=sortFunc)
    return matches_list

# Generates a score from 0-1 based on how many patterns within a piece can be found in the other
def similarity_score(notes1, notes2):
    """Returns a score from 0-1 of the similarity between two note lists

    Parameters
    ----------
    notes1 : list of NoteListElement objects
        a note list from the CorpusBase or ScoreBase methods
    notes2 : list of NoteListElement objects
        a note list from the CorpusBase or ScoreBase methods

    Returns
    -------
    final_score : int
        a score of similarity from 0-1
    """
    vectors1 = IntervalBase(notes1).generic_intervals
    vectors2 = IntervalBase(notes2).generic_intervals
    interval = 3
    scores = []
    while interval <= 6:
        # For each piece create a list of all patterns and then a list of unique patterns to compare against it
        pattern, patterns1, patterns_nodup1, patterns2, patterns_nodup2 = [], [], [], [], []

        for i in range(len(vectors1)-interval):
            pattern = []
            valid_pattern = True
            for num_notes in range(interval):
                if vectors1[i+num_notes].vector == 'Rest':
                    valid_pattern = False
                pattern.append(vectors1[i+num_notes].vector)
            if valid_pattern:
                patterns1.append(pattern)

        for j in range(len(vectors2)-interval):
            pattern = []
            valid_pattern = True
            for num_notes in range(interval):
                if vectors2[j+num_notes].vector == 'Rest':
                    valid_pattern = False
                pattern.append(vectors2[j+num_notes].vector)
            if valid_pattern:
                patterns2.append(pattern)

        for pat in patterns1:
            if pat not in patterns_nodup1:
                patterns_nodup1.append(pat)
        for pat2 in patterns2:
            if pat2 not in patterns_nodup2:
                patterns_nodup2.append(pat2)

        # With lists assembled we can do an easy comparison
        score = 0
        for a in patterns_nodup1:
            if patterns2.count(a) > 3:
                score += 1
            if patterns2.count(a) > 0:
                score += 1
            else:
                for b in patterns2:
                    diff = 0
                    for c in range(interval):
                        diff += abs(a[c] - b[c])
                    if diff == 1 or diff == 2:
                        #score += 0.5
                        break
        for d in patterns_nodup2:
            if patterns1.count(d) > 3:
                score += 1
            if patterns1.count(d) > 0:
                score += 1
            else:
                for e in patterns1:
                    diff = 0
                    for f in range(interval):
                        diff += abs(d[f] - e[f])
                    if diff == 1 or diff == 2:
                        #score += 0.5
                        break
        interval += 1
        scores.append(score / (len(patterns_nodup2) + len(patterns_nodup1)))
    final_score = (scores[0] + scores[1] + scores[2] + scores[3]) / 4
    return final_score

# Find all occurences of a specified pattern within a corpus
def find_motif(pieces: CorpusBase, motif: list, generic: bool = True):
    """Prints out all occurences of a specified motif

    Parameters
    ----------
    pieces : CorpusBase
        a CorpusBase object with all scores to be searched
    motif : list
        the motif in vectors (e.g. [-2,-2,2,-2,2])
    generic : bool, optional
        True to use generic vectors, False for semitone vectors- default is generic
    """
    # Assemble into patterns
    vectors = IntervalBase(pieces.note_list)
    if generic:
        patterns = into_patterns([vectors.generic_intervals], len(motif))
    else:
        patterns = into_patterns([vectors.semitone_intervals], len(motif))
    print("Finding instances of pattern " + str(motif) + ": ")
    # Find all occurences of given motif, print out information associated
    occurences = 0
    for pat in patterns:
        if motif == pat[0]:
            print("Selected pattern occurs in " + str(pat[1].metadata.title) + " part " + str(pat[1].part) + " beginning in measure " + str(pat[1].note.measureNumber) + " and ending in measure " + str(pat[2].note.measureNumber) + ". Note durations: " + str(pat[3]))
            occurences += 1
    print("Selected pattern occurs " + str(occurences) + " times.")

# Given list of matches, write to csv in current working directory
def export_to_csv(matches: list):
    """Exports matches data to a csv in the current working directory

    Parameters
    ----------
    matches : list
        return value from either find_exact_matches or find_close_matches
    """
    proceed = input("This method will create a csv file in your current working directory. Continue? (y/n): ").lower()
    csv_name = input("Enter a name for your csv file (.csv will be appended): ")
    csv_name += '.csv'
    if proceed != 'y' and proceed != 'yes':
        print("Exiting...")
        return
    import csv
    with open(csv_name, mode='w') as matches_file:
        matches_writer = csv.writer(matches_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        matches_writer.writerow(['Pattern Generating Match', 'Pattern matched', 'Piece Title', 'Part', 'First Note Measure Number', 'Last Note Measure Number', 'Note Durations', 'EMA', 'EMA url'])
        for match_series in matches:
            for match in match_series.matches:
                matches_writer.writerow([match_series.pattern, match.pattern, match.first_note.metadata.title, match.first_note.part, match.first_note.note.measureNumber, match.last_note.note.measureNumber, match.durations, match.ema, match.ema_url])
    print("CSV created in your current working directory.")

# For more naive usage- allows for user interaction, has return value of list of matches
# All features incorporated except non-whole piece selection
def assisted_interface():
    """Activates the assisted interface for more naive use

    Returns
    ----------
    matches : list
        list of PatternMatches based on the users various inputs
    """
    print("You can use ctrl-c to quit exit at any time. If you proceed through the entire process, the matches array will be returned from this function")
    urls = []
    url = input("Enter a url, or 'done' when finished: ")
    while url != 'done':
        urls.append(url)
        url = input("Enter a url, or 'done' when finished: ")
    corpus = CorpusBase(urls, [])
    vectors = IntervalBase(corpus.note_list)
    pattern_size = int(input("Enter the size of pattern you would like to analyze: "))
    interval_type = input("Enter 1 to match using generic intervals or enter 2 to match using semitone intervals: ")
    while interval_type != '1' and interval_type != '2':
        interval_type = input("Invalid input, enter 1 for generic intervals or 2 for semitone intervals: ")
    if interval_type == '1':
        patterns = into_patterns([vectors.generic_intervals], pattern_size)
    if interval_type == '2':
        patterns = into_patterns([vectors.semitone_intervals], pattern_size)
    min_matches = int(input("Enter the minimum number of matches needed to be displayed: "))
    close_or_exact = input("Enter 1 to include close matches or enter 2 for only exact matches: ")
    while close_or_exact != '1' and close_or_exact != '2':
        close_or_exact = input("Invalid input, enter 1 for close matches or 2 for only exact matches: ")
    if close_or_exact == '1':
        max_dif = int(input("Enter the maximum total distance threshold for a close match: "))
        matches = find_close_matches(patterns, min_matches, max_dif)
    if close_or_exact == '2':
        matches = find_exact_matches(patterns, min_matches)
    csv_results = input("Export results to CSV? (y/n): ").lower()
    if csv_results == 'y' or csv_results == 'yes':
        export_to_csv(matches)
    print_results = input("Print results? (y/n): ").lower()
    if print_results == 'y' or print_results == 'yes':
        if close_or_exact == '1':
            for item in matches:
                item.print_close_matches()
        if close_or_exact == '2':
            for item in matches:
                item.print_exact_matches()
    return matches

def compare_durations(durations1, durations2, threshold):
    """Used in classify_matches

    works similarly to find_close_matches in terms of its comparison technique
    """
    total = 0
    durations1_sum, durations2_sum = 0, 0
    for i in range(len(durations1)):
        total += abs(durations1[i]-durations2[i])
        durations1_sum += durations1[i]
        durations2_sum += durations2[i]
    if total <= threshold or durations1_sum == durations2_sum:
        return True
    else:
        return False

def sortMatches(match):
    """ Helper function for classify_matches
    """
    return match.first_note.offset


def classify_matches(exact_matches: list, durations_threshold = 2):
    """Classifies groups of matches into periodic entries, imitative duos, and fuga

    Classifies through offset comparison of matching melodic patterns, prints out information gathered.
    Reliably accurate results only guaranteed if exact_matches is generated from ONE piece.

    Parameters
    ----------
    exact_matches : list
        return value from find_exact_matches
    durations_threshold : int, optional
        maximum cumulative difference between two duration lists before they are deemed not similar, defaults to 2

    Returns
    -------
    classified_tuple : tuple
        classified_tuple[0] : list of lists of Match objects
            list of periodic entries, which are lists of Match objects
        classified_tuple[1] : list of lists of Match objects
            list of imitative_duos, which are lists of Match objects
        classified_tuple[0] : list of lists of Match objects
            list of fuga, which are lists of Match objects
    """
    # TO-DO: add in factoring for durations, narrow 80 beats window
    periodic_entries, im_duos, fuga = [], [], []
    for list_matches in exact_matches:
        offset_difs, offset_difs_info = [], []
        match_instance = list_matches.matches
        match_instance.sort(key = sortMatches)
        for index in range(len(match_instance) - 1):
            if compare_durations(match_instance[index + 1].durations, match_instance[index].durations, durations_threshold):
                offset_difs.append(match_instance[index + 1].first_note.offset -  match_instance[index].first_note.offset)
                offset_difs_info.append((match_instance[index], match_instance[index + 1]))
        i = 0
        while i < len(offset_difs) - 2:
            if offset_difs[i] > 64 or offset_difs[i + 1] > 64:
                pass
            elif offset_difs[i] == offset_difs[i + 1] and offset_difs[i] == offset_difs[i + 2]:
                grouping = (offset_difs_info[i][0], offset_difs_info[i][1], offset_difs_info[i + 1][0], offset_difs_info[i + 1][1], offset_difs_info[i + 2][0], offset_difs_info[i + 2][1])
                grouping = list(dict.fromkeys(grouping))
                periodic_entries.append(grouping)
            elif offset_difs[i] == offset_difs[i + 1]:
                grouping = (offset_difs_info[i][0], offset_difs_info[i][1], offset_difs_info[i + 1][0], offset_difs_info[i + 1][1])
                grouping = list(dict.fromkeys(grouping))
                periodic_entries.append(grouping)
            elif offset_difs[i] == offset_difs[i + 2]:
                grouping = (offset_difs_info[i][0], offset_difs_info[i][1], offset_difs_info[i + 2][0], offset_difs_info[i + 2][1])
                grouping = list(dict.fromkeys(grouping))
                im_duos.append(grouping)
            else:
                grouping = (offset_difs_info[i][0], offset_difs_info[i][1], offset_difs_info[i + 1][0], offset_difs_info[i + 1][1])
                grouping = list(dict.fromkeys(grouping))
                fuga.append(grouping)
            i += 1

    for entry in periodic_entries:
        print("Periodic Entry:")
        a = "Pattern: " + str(entry[0].pattern) + ", Locations in entry: "
        for b in entry:
            a += "\n- Measure " + str(b.first_note.note.measureNumber) + " in voice " + str(b.first_note.partNumber)
        print(a)
    for duo in im_duos:
        print("Imitative Duo:")
        a = "Pattern: " + str(duo[0].pattern) + ", Locations in entry: "
        for c in duo:
            a += "\n- Measure " + str(c.first_note.note.measureNumber) + " in voice " + str(c.first_note.partNumber)
        print(a)
    for f in fuga:
        print("Fuga:")
        a = "Pattern: " + str(f[0].pattern) + ", Locations in entry: "
        for d in f:
            a += "\n- Measure " + str(d.first_note.note.measureNumber) + " in voice " + str(d.first_note.partNumber)
        print(a)
    classified_tuple = (periodic_entries, im_duos, fuga)
    return classified_tuple
