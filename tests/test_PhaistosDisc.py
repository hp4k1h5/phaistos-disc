from phaistos_disc import (
    Direction,
    OutputType,
    PhaistosDisc,
    SideOrdering,
    data_fp,
    read_sign_map,
)


class TestPhaistosDisc:
    def test_ab_io(self):
        """Sides A->B, left to right (inside out)"""
        pd = PhaistosDisc(
            side_ordering=SideOrdering.a_b,
            direction=Direction.ltr,
        )

        assert ["side_a", "side_b"] == list(pd.data.keys())

        side_a = pd.data["side_a"]
        assert side_a[0] == ["38", "03", "10"]

    def test_ba_io(self):
        """Sides B->A, left to right (inside out)"""
        pd = PhaistosDisc(
            side_ordering=SideOrdering.b_a,
            direction=Direction.ltr,
        )

        assert ["side_b", "side_a"] == list(pd.data.keys())

        side_a = pd.data["side_b"]
        assert side_a[0] == ["07", "46", "45"]

    def test_ab_oi(self):
        """Sides A->B, right to left (outside in)"""
        pd = PhaistosDisc(
            side_ordering=SideOrdering.a_b,
            direction=Direction.rtl,
        )

        assert ["side_a", "side_b"] == list(pd.data.keys())

        side_a = pd.data["side_a"]
        assert side_a[0] == ["02", "12", "13", "01", "18", "46"]

    def test_ba_oi(self):
        """Sides B->A, right to left (outside in)"""
        pd = PhaistosDisc(
            side_ordering=SideOrdering.b_a,
            direction=Direction.rtl,
        )

        assert ["side_b", "side_a"] == list(pd.data.keys())

        side_a = pd.data["side_b"]
        assert side_a[0] == ["02", "12", "22", "40", "07"]

    def test_format_disc(self):
        pd = PhaistosDisc(
            side_ordering=SideOrdering.a_b,
            direction=Direction.ltr,
        )
        formatted = pd.format_disc()
        assert formatted[:8] == "A1 𐇵 𐇒 𐇙"

        formatted = pd.format_disc(prefix=False)
        assert formatted[:5] == "𐇵 𐇒 𐇙"

    def test_achterberg(self):
        pd = PhaistosDisc(
            side_ordering=SideOrdering.a_b,
            direction=Direction.outside_in,
        )
        achterberg_transcription = pd.format_disc(
            sign_map=read_sign_map(
                data_fp / "phaistos-disc_signs-achterberg.csv"
            ),
            output_type=OutputType.phoneme,
            letter_separator="-",
            word_separator="\n",
            prefix=False,
        )

        assert pd.data["side_a"][0] == ["02", "12", "13", "01", "18", "46"]
        assert achterberg_transcription.split("\n")[0] == "á-tu-mi1-SARU-s6-ti"
