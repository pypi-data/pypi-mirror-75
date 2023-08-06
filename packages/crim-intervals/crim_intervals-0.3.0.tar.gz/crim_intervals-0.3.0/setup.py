# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['crim_intervals']

package_data = \
{'': ['*']}

install_requires = \
['music21>=5.7.2,<6.0.0', 'requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'crim-intervals',
    'version': '0.3.0',
    'description': 'A python based, interactive music similarity engine',
    'long_description': "# An interval-analysis based music similarity engine\n\n## Find the project on Github and PyPI\n- [Github](https://github.com/HCDigitalScholarship/intervals)\n- [PyPI](https://pypi.org/project/crim-intervals/)\n\n## Project Goals:\n- Load mei file(s) from url or path\n- Carve out desired portion of piece/corpus\n- Create a sequence of interval objects from the score\n- Set filters on parts, measures, ids\n- Export EMA\n- Analyze similarity of two objects\n\n## Assisted Usage\nFor a guided way to get results for the basic intended usages of the project, simply enter:\n```\nassisted_interface()\n```\nwherever you are writing your code.\n\n## Method, Class help\nThe project is now documented with docstrings, for help using/understanding methods or classes use ```help(method_or_class_name)```\n\n## Example Usage\n- One piece at a time\n```\npiece1 = ScoreBase('https://crimproject.org/mei/CRIM_Model_0008.mei')\npiece2 = ScoreBase('https://sameplemeifile.mei')\nvectors1 = IntervalBase(piece1.note_list)\nvectors2 = IntervalBase(piece2.note_list_all_parts(1, 20))\npatterns = into_patterns([vector1.generic_intervals, vector.generic_intervals], 5)\nexact_matches = find_exact_matches(patterns, 10)\n```\n- Loading in a Corpus\n```\ncorpus = CorpusBase(['https://sameplemeifile1.mei', 'https://sameplemeifile.mei'],[/sample/path/to/mei/file, /sameple/path/two])\nvectors = IntervalBase(corpus.note_list)\npatterns = into_patterns([vectors.semitone_intervals], 5)\nclose_matches = find_close_matches(patterns, 10, 1)\n```\n- Outputting relevant information\n  - Printing out matches information\n  ```\n  ...\n  exact_matches = find_exact_matches(patterns, 10)\n  for item in exact_matches:\n      item.print_exact_matches()\n  close_matches = find_close_matches(patterns, 10, 1)\n  for item in close_matches:\n      item.print_close_matches()\n  ```\n  - Similarity scores\n  ```\n  piece1 = ScoreBase('https://crimproject.org/mei/CRIM_Model_0008.mei')\n  piece2 = ScoreBase('https://sameplemeifile.mei')\n  print(similarity_score(piece1.note_list, piece2.note_list, 5))\n  ```\n  - Outputting match information to csv (includes ema, mei slices)\n  ```\n  export_to_csv(exact_matches)\n  ```\n  - Find occurences of a motif\n  ```\n  find_motif(CorpusBase object, [motif], generic intervals boolean-optional)\n  ```\n\n## Usage Flow ~~~\n- Load in files with either ScoreBase or CorpusBase\n  ```\n  ScoreBase(url)\n  CorpusBase([url1, url2, ...], [filepath1, filepath2, ...])\n  ```\n  - Search for a motif:\n  ```\n  find_motif(corpus: CorpusBase, [motif], generic intervals: boolean)\n  ```\n- Create desired note list for use in IntervalBase\n  - Options using CorpusBase:\n    ```\n    piece.note_list\n    ```\n  - Options using ScoreBase:\n    ```\n    piece.note_list\n    piece.note_list_down_beats\n    piece.note_list_selected_beats([beats])\n    piece.note_list_all_parts(starting_measure, number_of_measures_after)\n    piece.note_list_single_part(part_number, starting_measure, number_of_measures_after)\n    piece.note_list_by_offset([offsets])\n    ```\n- At this point similarity scores can be shown\n  - size of pattern indicates how many notes in a row need to follow the same rhythmic pattern to be considered a match\n```\nsimilarity_score(first piece note list, second piece note list)\n```\n- Decide between semitone intervals and generic intervals\n```\nvectors.generic_intervals\nvectors.semitone_intervals\n```\n- Construct patterns from note_list (more options for pattern construction forthcoming)\n```\ninto_patterns([list of piece note lists], size of pattern)\n```\n- Decide which type of matches to find\n  - These will not work if you don't send it the return value from into_patterns\n```\nfind_exact_matches(return value from into_patterns, minimum matches needed to be displayed)\nfind_close_matches(return value from into_patterns, minimum matches needed to be displayed, threshold)\n```\n  - Returns a list of matches for easy analysis, printing shown above\n- Export to csv in current working directory:\n```\nexport_to_csv(exact_matches)\n```\n- Classify matches into periodic entries, imitative duos, or fuga in an attempt to highlight similarity\n  - durations_threshold is the cumulative rhythmic difference acceptable for patterns to be classified\n```\nclassify_matches(exact_matches, durations_threshold-optional)\nclassify_matches(close_matches, durations_threshold-optional)\n```\n- Run desired analysis with your own python code, print out results, etc.\n",
    'author': 'Freddie Gould',
    'author_email': 'fgould@haverford.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
