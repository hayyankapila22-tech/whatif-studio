# HIW23 — How does a mosquito find you? Bubbly Liam voice, no studies, "So," loop.
SENTENCES = [
    dict(cap="How does a mosquito *find* you in the dark?", gap=0.2),
    dict(cap="Step one: || your *breath*!", gap=0.15),
    dict(cap="You breathe out *carbon dioxide*, || and they can sense it || from about *15 metres* away.", say="You breathe out carbon dioxide, and they can sense it from about fifteen metres away.", weights={"15": 2}, gap=0.2),
    dict(cap="Step two: || your *smell*.", gap=0.15),
    dict(cap="Tiny germs on your skin || make a scent they *love*. || That's why some people get bitten way *more*!", gap=0.2),
    dict(cap="Step three: || up close, || they feel your body *heat*.", gap=0.2),
    dict(cap="And only the *females* bite. || They need your blood || to make *eggs*!", gap=0.2),
    dict(cap="The trick: || loose *clothes* || block the bite || and hide your heat.", gap=0.4),
    dict(cap="So,", gap=0.0),
]
