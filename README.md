# Phaistos Disc

> A library of Python utilities to aid in the decipherment of the Phaistos disc

![Sides A and B of the Phaistos disc](./src/phaistos_disc/data/phaistos-disc.png)

Since 1908[^1], the Phaistos disc has eluded decipherment, despite widespread interest and several recent computer-aided analyses[^2]. The utilities provided in this library aim to assist in the analysis and decipherment of the Phaistos disc by providing a suite of tools and databases, and by documenting progress made by means of computational or analytical advancements.

Some research materials are included in [/biblio/](./biblio)

## Fonts

An overview of the unicode glyph set is available from [wikipedia](https://en.wikipedia.org/wiki/Phaistos_Disc_(Unicode_block)). There are several fonts that currently display a range of the Phaistos Disc Unicode block, some of which can be found [here](https://www.fileformat.info/info/unicode/block/phaistos_disc/fontsupport.htm). Every computer, terminal and text processor will handle these codepoints differently but each will need to be configured if you are having trouble seeing the glyphs.

I have found [Everson Mono](https://www.fileformat.info/info/unicode/font/eversonmono/index.htm) to be the most reliable.

## Usage

### Basic text formatting

```python
# Print the disc with line+word numbering
from phaistos_disc import format_disc

pd = PhaistosDisc()
print(pd.format_disc())

A1 𐇑 𐇛 𐇜 𐇐 𐇡 '𐇽
A2 𐇧 𐇷 𐇛
A3 𐇬 𐇼 𐇖 '𐇽
A4 𐇬 𐇬 𐇱
A5 𐇑 𐇛 𐇓 𐇷 𐇰
…

# Print the disc with line separators
print(pd.format_disc(
    letter_separator="-", word_separator="|", prefix=False,
))

𐇑-𐇛-𐇜-𐇐-𐇡-'𐇽|𐇧-𐇷-𐇛|𐇬-𐇼-𐇖-'𐇽|𐇬-𐇬-𐇱|𐇑-𐇛-𐇓-𐇷-𐇰
```

### Transliteration

As an example of the potential utility of the tool, I've included Achterberg's transcriptional mapping[^3] of phonetic values to their hieroglyphic forms in [](./src/data/phaistos-disc_signs-achterberg.csv), which can be used as shown below:

```python
# Following Achterberg 2021, _The Phaistos Disc: A Luwian Letter to Nestor_
from phaistos_disc import PhaistosDisc

pd = PhaistosDisc(
   side_ordering=SideOrdering.a_b,
   direction=Direction.io,
)
achterberg_transliteration = pd.format_disc(
   sign_map=pd.get_sign_map(data_fp / "phaistos-disc_signs-achterberg.csv"),
   output_type=OutputType.phoneme,
   letter_separator="-",
   word_separator="\n",
   prefix=True,
)

print(achterberg_translisteration)

A1 á-tu-mi1-SARU-s6-ti
A2 pa-ya-tu
A3 u-ná-sa2-ti
A4 u-u-ri
A5 á-tu-hi-ya-wa8
…
```

By modifying an existing transliteration or adding a new csv file to the [](`/phaistos_disc/data/`) directory, you can generate a phonetic transliteration of the entire disc.

### Sign Maps

There are currently several sign_maps in [](./src/phaistos_disc/data/). These are intended to provide a familiar interface for users to interact with the tool on a case-by-case basis. For larger analytical purposes, one can directly construct a sign_map as a polars DataFrame and pass it to `PhaistosDisc.format_disc()` or other function.

Generally, try to use the polars `sign_map_schema` in `src/phaistos_disc/util` when constructing your own dataframes. If you are not using a column listed there, then it shouldn't be necessary to include that column, but `number` is required.


### Decipherment

The primary focus of this library is to provide a suite of tools that aid in the decipherment of the disc. The general method pursued initially will be to:

- create combinations of symbol-to-phoneme mappings
- generate a transliteration
- compare the transliteration with known ancient Mediterranean languages

If a particular symbol-phoneme mapping produces a set of words that can be found in another language. Achterberg (2021) and others have done similar work without the use of computational means, relying on the disc's symbols' pictographic resemblance to other known hieroglyphic symbols. But consensus has not been reached as to the correctness of any particular transcription or translation.

#### Decipherment Challenges

A good summary of challenges regarding reading and interpreting the disc are available from [this letter to the unicode consortium](https://www.unicode.org/L2/L2011/11166-phaistos-response.pdf).

##### Disc Side Ordering

The disc is inscribed on both sides. There is no consensus on which side is to be read first, or if both sides may be read independently without relation one to the other. This library provides transpose facilities for either.

##### Writing/Reading Direction

The disc does not provide obvious signs indicating whether to read from the periphery toward the center (right-to-left) or from the center outward toward the periphery (left-to-right). There appears to be a majority opinion that the disc should be read (or was, at least, probably written) from the exterior, clockwise, circling towards the center, from right to left. Several signs face the opposite direction, towards the right, and some scholars have inferred an inscriptional directionality from this, i.e. that the script should be read in the same direction as that in which the figures are facing or walking. This library accepts either as parameters to various facilities.

##### Signs and Phonetic Values

It is not known for certain whether each symbol (glyph) represents a letter (alphabetically), a syllable (syllabically), a word (hieroglyphically), or a combination of these as seen in Linear B and elsewhere. The script found in the disc is likely to be a syllabary given the number of symbols found and their distribution.

- There are 45 unique glyphs and a 46th combining stroke
- There are 61 unique words

> ⚠️ work in progress
`PhaistosDisc().get_stats()` provides some of these counts


> ⚠️ work in progress
`PhaistosDisc().get_ngrams()` provides some analytical capabilities

### Install

1. Download the library, either by pip installing it

- `pip install phaistos-disc`, or
  <!-- - `pip install phaistos-disc[biblio]` to include reference works -->

2. or cloning this repo. phaistos-disc uses [`uv`](https://docs.astral.sh/uv/) to structure and manage the project.

- [Install `uv`](https://docs.astral.sh/uv/getting-started/installation/)
- `git clone https://github.com/hp4k1h5/phaistos-disc.git`
- `cd` into the project with e.g. `cd path/to/phaistos-disc`
- Create a virtual environment: `uv venv`
- Create a venv shell: `source .venv/bin/active`
- Install dependencies: `uv sync`

## Contributions

Contributions are welcome. Fork the repo, follow the installation instructions above, and submit a pull review with your edits.

## Bibliography

[^1]: Evans, Arthur. 1952. _Scripta Minoa, the Written Documents of Minoan Crete, with Special Reference to the Archives of Knossos._ Oxford: Clarendon Press.

[^2]: Braović, Maja, Damir Krstinić, Maja Štula, and Antonia Ivanda. 2024. “A Systematic Review of Computational Approaches to Deciphering Bronze Age Aegean and Cypriot Scripts.” Computational Linguistics 50 (2): 725–79. https://doi.org/10.1162/coli_a_00514.

[^3]: Achterberg, Winfried. 2021. “The Phaistos Disc : A Luwian Letter to Nestor.” The Phaistos Disc : A Luwian Letter to Nestor, January. https://www.academia.edu/66972374/The_Phaistos_disc_a_Luwian_letter_to_Nestor.
