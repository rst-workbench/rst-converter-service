# rst-converter-service
REST API to convert between different Rhetorical Structure Theory file formats.
It is built on top of the [discoursegraphs](http://github.com/arne-cl/discoursegraphs) library.

# Supported Input Formats

- CODRA
- dis (e.g. used by RST-DT corpus)
- DPLP
- Heilman/Sagae (2015)
- rs3
- HILDA (also used by Feng/Hirst 2014)
    - **Note**: We don't use the original HILDA format, but a slightly adapted one based
      on the internal nltk.Tree representation.
    - [arne-cl/feng-hirst-rst-parser](https://github.com/arne-cl/feng-hirst-rst-parser),
      [nlpbox/feng-hirst-service](https://github.com/nlpbox/feng-hirst-service) and
      [nlpbox/hilda-service](https://github.com/nlpbox/hilda-service) can produce
      this format.
    
## original HILDA format

```
(Contrast[S][N]
  _!Although they did n't like it ,!_
  _!they accepted the offer . <P>!_)
```

## adapted HILDA format

```
ParseTree('Contrast[S][N]', ["Although they did n't like it ,", 'they accepted the offer .'])
```

# Supported Output Formats

- dis
- rs3
- rstlatex (for embedding RST trees into LaTeX documents)
- tree.prettyprint (ASCII-style tree)
- svgtree (SVG image of an nltk Tree)
- svgtree-base64 (base64 encoded SVG image of an nltk Tree)

# Installation

The simplest way to install the rst-converter-service is using Docker:

```
git clone https://github.com/nlpbox/rst-converter-service.git
cd rst-converter-service/
docker build -t rst-converter-service .
```

# Usage

To run the web service, type:

```
docker run -p 5000:5000 -ti rst-converter-service
```

In another terminal, you can now convert RST files. To convert the file `car-repair.rs3`
from `rs3` format to `dis` format, type:

```
curl -XPOST localhost:5000/convert/rs3/dis -F input=@car-repair.rs3
(Root
  (span 1 2)
  (Satellite
    (leaf 1)
    (rel2par background)
    (text
      _!I am having my car repaired in Santa Monica (1522 Lincoln Blvd.) this Thursday 19th._!))
  (Nucleus
    (leaf 2)
    (rel2par span)
    (text
      _!Would anyone be able to bring me to ISI from there by 5 pm please?_!)))
```

For "visualizing" the RST tree, you might try prettyprinted trees:

```
curl -XPOST localhost:5000/convert/rs3/tree.prettyprint -F input=@car-repair.rs3
                 background
        _____________|______________
       S                            N
       |                            |
I am having my               Would anyone be
car repaired in             able to bring me
 Santa Monica (                to ISI from
 1522 Lincoln                 there by 5 pm
  Blvd.) this                    please?
 Thursday 19th.
```

To see all supported input and output formats, type

```
curl localhost:5000/input-formats
["codra", "dis", "dplp", "hilda", "hs2015", "rs3"]
```

or

```
curl localhost:5000/output-formats
["dis", "rs3", "tree.png", "tree.png-base64", "tree.prettyprint"]
```

# Citation

If you use the rst-converter-service in your academic work, please cite the following paper:

Neumann, A. 2015. [discoursegraphs: A graph-based merging tool and converter
for multilayer annotated corpora](https://www.aclweb.org/anthology/W15-1843). In *Proceedings of the 20th Nordic Conference
of Computational Linguistics (NODALIDA 2015)*, pp. 309-312.

```
 @inproceedings{neumann2015discoursegraphs,
   title={discoursegraphs: A graph-based merging tool and converter for multilayer annotated corpora},
   author={Neumann, Arne},
   booktitle={Proceedings of the 20th Nordic Conference of Computational Linguistics (NODALIDA 2015)},
   pages={309-312},
   year={2015}
 }
 ```
