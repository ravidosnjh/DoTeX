"""Define LaTeX code to be used in toolbar classes

Variables
---------
greek_letters : dict
capital_greek_letters : dict
var_greek_letters : dict
letters : list
capital_letters : list
var_letters : list
arrows : dict
arrow_symbols : list
relations : dict
relation_symbols : list
miscs : dict
misc_symbols : list
reservedc : dict
operators : list
brackets : dict
envrionments : list
a : list
b : list
c : list
d : list
e : list
f: list
g : list
h : list
i : list
j : list
k : list
l : list
m : list
n : list
o : list
p : list
r : list
s : list
t : list
u : list
v : list
w : list
x : list
y : list
z : list
commands : list
"""
# Greek Letters
greek_letters = dict()
capital_greek_letters = dict()
var_greek_letters = dict()
letters = [("α", "alpha"), ("β", "beta"), ("γ", "gamma"), ("δ", "delta"), ("ε", "epsilon"), ("ζ", "zeta"), ("η", "eta"),
            ("θ", "theta"), ("ι", "iota"), ("κ", "kappa"), ("λ", "lambda"), ("μ", "mu"), ("ν", "nu"), ("ξ", "xi"),
            ("ο", "o"), ("π", "pi"), ("ρ", "rho"), ("σ" ,"sigma"), ("τ", "tau"), ("υ", "upsilon"), ("φ", "phi"),
            ("χ", "chi"), ("ψ", "psi"), ("ω", "omega")]

capital_letters = [("Α", "A"), ("Β", "B"), ("Γ", "Gamma"), ("Δ", "Delta"), ("Ε", "E"), ("Ζ", "Z"), ("Η", "H"),
                   ("Θ", "Theta"), ("Ι", "I"), ("Κ", "K"), ("Λ", "Lambda"), ("Μ", "M"), ("Ν", "N"), ("Ξ", "Xi"),
                   ("Ο", "O"), ("Π", "Pi"), ("Ρ", "P"), ("Σ", "Sigma"), ("Τ", "T"), ("Υ", "Upsilon"), ("Φ", "Phi"),
                   ("Χ", "X"), ("Ψ", "Psi"), ("Ω", "Omega")]

var_letters = [("varepsilon", "varepsilon"), ("ς", "varsigma"), ("ϑ", "vartheta"), ("varphi", "varphi"),
               ("varrho", "varrho")]

for letter, code in letters:
    greek_letters[letter] = f"\\{code}"
for letter, code in capital_letters:
    if len(code) == 1:
        capital_greek_letters[letter] = code
    else:
        capital_greek_letters[letter] = f"\\{code}"
for letter, code in var_letters:
    var_greek_letters[letter] = f"\\{code}"


# Symbols
arrows = dict()
arrow_symbols = [("←", "leftarrow"), ("⇒", "Leftarrow"), ("→", "rightarrow"), ("⇒", "Rightarrow"),
                 ("↔", "leftrightarrow"), ("⇌", "rightleftharpoons"), ("↑", "uparrow"), ("↓", "downarrow"),
                 ("⇑", "Uparrow"), ("⇓", "Downarrow"), ("⇔", "Leftrightarrow"), ("⇕", "Updownarrow"), ("↦", "mapsto"),
                 ("−↦", "longmapsto"), ("↗", "nearrow"), ("↘", "searrow"), ("↙", "swarrow"), ("↖", "nwarrow"),
                 ("↼", "leftharpoonup"), ("⇀", "rightharpoonup"), ("↽", "leftharpoondown"), ("⇁", "rightharpoondown")]

for arrow, code in arrow_symbols:
    arrows[arrow] = f"\\{code}"

relations = dict()
relation_symbols = [("×", "times"), ("·", "cdot"), ("÷", "div"), ("∩", "cap"), ("∪", "cup"), ("≠", "neq"), ("≤", "leq"),
                    ("≥", "geq"), ("∈", "in"), ("⊥", "perp"), ("∉", "notin"), ("⊂", "subset"), ("≃", "simeq"),
                    ("≈", "approx"), ("∧", "wedge"), ("∨", "vee"), ("⊕", "oplus"), ("⊗", "otimes"), ("□", "Box"),
                    ("⊠", "boxtimes"), ("≡", "equiv"), ("≅", "cong")]

for relation, code in relation_symbols:
    relations[relation] = f"\\{code}"

miscs = dict()
misc_symbols = [("∞", "infty"), ("∀", "forall"), ("ℜ", "Re"), ("ℑ", "Im"), ("∇", "nabla"), ("∃", "exists"),
                 ("∂", "partial"), ("∄", "nexists"), ("{}", "emptyset"), ("∅", "varnothing"), ("℘", "wp"),
                 ("C", "complement"), ("¬", "neg"), ("···", "cdots"), ("□", "square"), ("√", "surd"),
                 ("∎", "blacksquare"), ("△", "triangle")]

for misc, code in misc_symbols:
    miscs[misc] = f"\\{code}"

reservedc = {"#": "\\#", "$": "\\$", "%": "\\%", "^": "\\verb1^1", "&": "\\&", "_": "\\_", "{ }": "\\{ \\}",
             "~": "\\verb1~1", "\\": "\\verb1\\1"}

operators = ["\\sin", "\\cos", "\\tan", "\\sinh", "\\cosh", "\\tanh", "\\arcsin", "\\arccos", "\\arctan", "\\sec",
             "\\csc", "\\cot", "\\coth", "\\exp", "\\ker", "\\min", "\\max", "\\ln", "\\log", "\\deg", "\\gcd", "\\lg",
             "\\Pr", "\\sup", "\\det", "\\hom", "\\lim", "\\liminf", "\\limsup", "\\arg", "\\dim"]

brackets = {"( )":("(", ")"), "[ ]": ("[", "]"), "{ }": ("\\{", "\\}"), "< >": ("\\langle", "\\rangle"),
            "| |": ("|", "|"), "|| ||": ("\\|", "\\|"), "⌈ ⌉": ("\\lceil", "\\rceil"), "⌊ ⌋": ("\\lfloor", "\\rfloor")}

environments = ["\\begin{abstract}", "\\end{abstract}", "\\begin{array}{lrc}", "\\end{array}{lrc}",
                "\\begin{center}", "\\end{center}", "\\begin{description}", "\\end{description}",
                "\\begin{displaymath}", "\\end{displaymath}", "\\begin{document}", "\\end{document}",
                "\\begin{enumerate}", "\\end{enumerate}","\\begin{eqnarray}", "\\end{eqnarray}", "\\begin{eqnarray*}",
                "\\end{eqnarray*}", "\\begin{equation}", "\\end{equation}", "\\begin{figure}[pos]",
                "\\end{figure}[pos]", "\\begin{figure*}[pos]", "\\end{figure*}[pos]", "\\begin{flushleft}",
                "\\end{flushleft}", "\\begin{flushright}", "\\end{flushright}", "\\begin{itemize}", "\\end{itemize}",
                "\\begin{list}{labeling}{spacing}", "\\end{list}{labeling}{spacing}", "\\begin{math}", "\\end{math}",
                "\\begin{minipage}[pos]{vsize}", "\\end{minipage}[pos]{vsize}", "\\begin{picture}(x, y)(xl, yl)",
                "\\end{picture}(x, y)(xl, yl)", "\\begin{quotation}", "\\end{quotation}", "\\begin{quote}",
                "\\end{quote}", "\\begin{tabbing}", "\\end{tabbing}", "\\begin{table}[pos]", "\\end{table}[pos]",
                "\\begin{table*}[pos]", "\\end{table*}[pos]", "\\begin{tabular}{arg}", "\\end{tabular}{arg}",
                "\\begin{theorem}", "\\end{theorem}", "\\begin{titlepage}", "\\end{titlepage}", "\\begin{verbatim}",
                "\\end{verbatim}", "\\begin{verse}", "\\end{verse}"]

a = ["\\a’", "\\a‘", "\\a=", "\\aa", "\\acute", "\\addcontentsline{toc}{section}{name}", "\\address{text}",
     "\\addtocontents{toc}{text}", "\\addtocounter{name}{amount}", "\\addtolength{\\nl}{length}", "\\ae", "\\aleph",
     "\\alph{counter}", "\\alpha", "\\amalg", "\\and", "\\angle", "\\appendix", "\\approx", "\\arabic{counter}",
     "\\arccos", "\\arcsin", "\\arctan", "\\arg", "\\arraycolsep", "\\arrayrulewidth", "\\arraystretch", "\\ast",
     "\\asymp", "\\author{names}"]

b = ["\\b", "\\backslash", "\\bar", "\\baselineskip", "\\baselinestretch", "\\beta", "\\bf", "\\bibitem{ref}",
     "\\bibliography{file}", "\\bibliographystyle{style}", "\\bigcap", "\\bigcirc", "\\bigcup", "\\bigodot",
     "\\bigoplus", "\\bigotimes", "\\bigtriangledown", "\\bigtriangleup", "\\bigskip", "\\bigskipamount", "\\bigsqcup",
     "\\biguplus", "\\bigvee", "\\bigwedge", "\\bmod", "\\boldmath", "\\bot", "\\bottomfraction", "\\bowtie", "\\Box",
     "\\breve", "\\bullet"]
c = ["\\c", "\\cal", "\\cap", "\\caption[loftitle]{text}", "\\cc{text}", "\\cdot", "\\cdots", "\\centering",
     "\\chapter[toctitle]{text}", "\\chapter*{title}", "\\check", "\\chi", "\\circ", "\\circle{diameter}",
     "\\circle*{diameter}", "\\cite[subcit]{ref}", "\\cleardoublepage", "\\clearpage", "\\cline{i-j}",
     "\\closing{text}", "\\clubsuit", "\\columnsep", "\\columnseprule", "\\columnwidth", "\\cong", "\\coprod",
     "\\copyright", "\\cos", "\\cosh", "\\cot", "\\coth", "\\csc", "\\cup"]

d = ["\\d", "\\dag", "\\dagger", "\\dashbox{dwid}(width,height)[pos]{text}", "\\dashv", "\\date{adate}", "\\day",
     "\\dblfloatpagefraction", "\\dblfloatsep", "\\dbltextfloatsep", "\\dbltopfraction", "\\ddag", "\\ddagger",
     "\\ddot", "\\ddots", "\\deg", "\\delta", "\\det", "\\diamond", "\\diamondsuit", "\\dim", "\\displaystyle", "\\div",
     "\\documentstyle[substy]{sty}", "\\dot", "\\doteq", "\\dotfill", "\\doublerulesep", "\\downarrow"]

e = ["\\ell", "\\em", "\\emptyset", "\\encl{text}", "\\epsilon", "\\equiv", "\\eta", "\\evensidemargin", "\\exists",
     "\\exp"]

f = ["\\fbox{text}", "\\fboxrule", "\\fboxsep", "\\fill", "\\flat", "\\floatpagefraction", "\\floatsep", "\\flushbottom",
     "\\fnsymbol{counter}", "\\footheight", "\\footnote{text}", "\\footnotemark", "\\footnotesep", "\\footnotesize",
     "\\footskip", "\\footnotetext{text}", "\\footnotemark", "\\forall is ∀ (math mode)",
     "\\frac{numerator}{denominator}", "\\frame{text}", "\\framebox[size][pos]{text}",
     "\\framebox(width,height)[pos]{text}", "\\frown", "\\fussy"]

g = ["\\gamma", "\\gcd", "\\ge", "\\geq", "\\gets", "\\gg", "\\glossary{text}", "\\glossaryentry{text}{ref}", "\\grave"]

h = ["\\H", "\\hat", "\\hbar", "\\headheight", "\\headsep", "\\heartsuit", "\\hfill", "\\hline", "\\hom",
    "\\hookleftarrow", "\\hookrightarrow", "\\hrulefill", "\\hspace{len}", "\\hspace*{len}", "\\huge",
    "\\hyphenation{wordlist}"]

i = ["\\i", "\\iff", "\\Im", "\\imath", "\\in", "\\include{filename}", "\\includeonly{file1,file2}", "\\index{text}",
     "\\indexentry{text}{ref}", "\\indexspace", "\\inf", "\\infty", "\\input{file}", "\\int", "\\intextsep", "\\iota",
     "\\it", "\\item[text]", "\\itemindent", "\\itemsep"]

j = ["\\j", "\\jmath", "\\Join"]

k = ["\\kappa", "\\ker", "\\kill"]

l = ["\\l", "\\label{text}", "\\labelwidth", "\\labelsep", "\\lambda", "\\land", "\\langle", "\\large", "\\Large",
     "\\LARGE", "\\LaTeX", "\\lbrace", "\\lbrack", "\\lceil", "\\ldots", "\\le", "\\leadsto", "\\left*", "\\leftarrow",
     "\\lefteqn{formula}", "\\leftharpoondown", "\\leftharpoonup", "\\leftmargin", "\\leftrightarrow", "\\leq",
     "\\lfloor", "\\lg", "\\lhd", "\\lim", "\\liminf", "\\limsup", "\\line(x,y){len}", "\\linebreak[n]",
     "\\linethickness{dimen}", "\\linewidth", "\\listoffigures", "\\listoftables", "\\listparindent", "\\ll", "\\ln",
     "\\lnot", "\\log", "\\longleftarrow", "\\longleftrightarrow", "\\Longleftrightarrow", "\\longmapsto",
     "\\longrightarrow", "\\lor", "\\lq"]

m = ["\\makebox", "\\makeglossary", "\\makeindex", "\\maketitle", "\\mapsto", "\\marginpar{text}", "\\marginparpush",
     "\\marginparsep", "\\marginparwidth", "\\markboth{lhd}{rhd}", "\\markright{rhd}", "\\max", "\\mbox{text}",
     "\\medskip", "\\medskipamount", "\\mho", "\\mid", "\\min", "\\mit", "\\models", "\\month", "\\mp", "\\mu",
     "\\multicolumn{noc}{fmt}{text}", "\\multiput(x, y)(∆x, ∆y){n}{obj}"]

n = ["\\nabla", "\\natural", "\\ne", "\\nearrow", "\\neg", "\\neq", "\\newcommand{\\cs}[narg]{def}",
     "\\newcounter{counter}[name]", "\\newenvironment{envname}[narg]{def1}{def2}", "\\newfont{cs}{name}",
     "\\newlength{\\nl}", "\\newline", "\\newpage", "\\newsavebox{\\binname}", "\\newtheorem{env}[env2]{label}[sectyp]",
     "\\ni", "\\nofiles", "\\noindent", "\\nolinebreak[n]", "\\nonumber", "\\nopagebreak[n]", "\\normalmarginpar",
     "\\reversemarginpar", "\\normalsize", "\\not", "\\notin", "\\nu", "\\nwarrow"]
o = ["\\o", "\\O", "\\obeycr", "\\oddsidemargin", "\\odot", "\\oe", "\\oint", "\\omega", "\\Omega", "\\ominus",
     "\\onecolumn", "\\opening{text}", "\\oplus", "\\oslash", "\\otimes", "\\oval(x,y)", "\\overbrace{text}",
     "\\overline{text}", "\\owns"]

p = ["\\P", "\\pagebreak[n]", "\\pagenumbering{style}", "\\pageref{text}", "\\pagestyle{sty}",
     "\\paragraph[toctitle]{text}", "\\paragraph*{text}", "\\parallel", "\\parbox[pos]{size}{text}", "\\parindent",
     "\\parsep", "\\parskip", "\\part[toctitle]{text}", "\\part*{text}", "\\partial", "\\partopsep", "\\perp", "\\phi",
     "\\pi", "\\pm", "\\pmod{modulus}", "\\poptabs", "\\pounds", "\\Pr", "\\prec", "\\preceq", "\\prime", "\\prod",
     "\\propto", "\\protect", "\\ps", "\\psi", "\\pushtabs", "\\put(x,y){stuff}"]

r = ["\\raggedbottom", "\\raggedleft", "\\raggedright", "\\raisebox{dim}[d2][d3]{text}", "\\rangle", "\\rbrace",
     "\\rbrack", "\\rceil", "\\Re", "\\ref{text}", "\\renewcommand{\\cs}[narg]{def}",
     "\\renewenvironment{envname}[narg]{def1}{def2}", "\\newenvironment", "\\restorecr", "\\reversemarginpar",
     "\\rfloor", "\\rhd", "\\rho", "\\right*", "\\rightarrow", "\\rightharpoondown", "\\rightharpoonup",
     "\\rightleftharpoons", "\\rightmargin", "\\rm", "\\roman{counter}", "\\rq", "\\rule[height]{length}{width}"]

s = ["\\savebox{\\binname}[width][pos]{text}", "\\sbox{\\binname}{text}", "\\sc", "\\scriptsize", "\\scriptstyle",
     "\\scriptscriptstyle", "\\searrow", "\\sec", "\\section[toctitle]{text}", "\\section*{text}",
     "\\setcounter{counter}{value}", "\\setlength{\\nl}{length}", "\\setminus", "\\settowidth{\\nl}{text}", "\\sf",
     "\\sharp", "\\shortstack[pos]{x\\\\yy\\\\zzz}", "\\sigma", "\\Sigma", "\\signature{text}", "\\sim", "\\simeq",
     "\\sin", "\\sinh", "\\sl", "\\sloppy", "\\small", "\\smallint", "\\smallskip", "\\smallskipamount", "\\smile",
     "\\spadesuit", "\\sqcap", "\\sqcup", "\\sqrt[3]{arg}", "\\sqsubset", "\\sqsubseteq", "\\sqsupset", "\\sqsupseteq",
     "\\ss", "\\stackrel{stuff}{delim}", "\\star", "\\stop", "\\subparagraph[toctitle]{text}", "\\subparagraph*{text}",
     "\\subsection[toctitle]{text}", "\\subsubsection[toctitle]{text}", "\\subsection*{text}", "\\subsubsection*{text}",
     "\\subset", "\\subseteq", "\\succ", "\\succeq", "\\sum", "\\sup", "\\supset", "\\supseteq", "\\surd", "\\swarrow",
     "\\symbol{cc}"]

t = ["\\t", "\\tabbingsep", "\\tabcolsep", "\\tableofcontents", "\\tan", "\\tanh", "\\tau", "\\TeX", "\\textfloatsep",
     "\\textfraction", "\\textheight", "\\textstyle", "\\textwidth", "\\thanks{footnote}", "\\theta", "\\Theta",
     "\\thicklines", "\\thinlines", "\\thinspace", "\\thispagestyle{sty}", "\\tilde", "\\times", "\\tiny",
     "\\title{text}", "\\to", "\\today", "\\top", "\\topfraction", "\\topmargin", "\\topsep", "\\topskip",
     "\\triangleleft", "\\triangleright", "\\tt", "\\twocolumn[text]", "\\typein[\\cs]{text}", "\\typeout{text}"]

u = ["\\u", "\\unboldmath", "\\underbrace{text}", "\\underline{text}", "\\unitlength", "\\unlhd", "\\unrhd",
     "\\uparrow", "\\updownarrow", "\\uplus", "\\upsilon", "\\Upsilon", "\\usebox{\\binname}", "\\usecounter{counter}"]

v = ["\\v", "\\value{counter}", "\\varepsilon", "\\varphi", "\\varpi", "\\varrho", "\\varsigma", "\\vartheta",
     "\\vdash", "\\vdots", "\\vec", "\\vector(x,y){len}", "\\vee", "\\verb/text/", "\\verb*/text/", "\\vert", "\\Vert",
     "\\vfill", "\\vspace{len}", "\\vspace*{len}"]

w = ["\\widehat{arg}", "\\widetilde{arg}", "\\wp", "\\wr"]

x = ["\\xi"]

y = ["\\year"]

z = ["\\zeta"]

commands = [a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, r, s, t, u, v, w, x, y, z]
