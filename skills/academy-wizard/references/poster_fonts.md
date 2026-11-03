# Poster font provenance

- Latin: existing bundled `lato2-bold.woff`, Lato Bold (700); SIL Open Font License in `assets/fonts/lato-OFL.txt`.
- Japanese: existing repository `courses/open-chiplet-economy/locales/ja-JP/fonts/NotoSansJP[wght].ttf`, instantiated at weight 700 and subset to the Japanese poster's text. License copied from its adjacent `NotoSansJP-OFL.txt`.
- Korean: [Google Fonts Noto Sans KR](https://github.com/google/fonts/tree/main/ofl/notosanskr), `NotoSansKR[wght].ttf`, instantiated at weight 700 and subset to the Korean poster's text. License copied from the same directory's `OFL.txt`.

The Noto subsets retain the original font's glyph outlines; `poster-locale-fonts.json` records covered text characters and maps locales to files. To extend either subset, use fontTools and Brotli: open the original TTF with `TTFont`, call `instantiateVariableFont(font, {"wght": 700}, inplace=True)`, collect all badge/title/support characters from that locale's `poster.json` files, use `Subsetter.populate(text=characters)` and `Subsetter.subset(font)`, then set `font.flavor = "woff2"` and save. Update the matching `characters` inventory, retain the OFL license, rebuild and inspect the locale. The subset font is not a substitute for a complete locale font in course content.
