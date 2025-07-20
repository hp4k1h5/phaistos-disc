from phaistos_disc import PhaistosDisc

pd = PhaistosDisc()
fmt = pd.format_disc(
    letter_separator="-",
    word_separator="|",
    prefix=False,
)

print(fmt)
