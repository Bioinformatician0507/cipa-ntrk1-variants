# CIPA and NTRK1: can a model tell pathogenic from benign?

I first read about CIPA (congenital insensitivity to pain with anhidrosis) in my first year of college, in a paper about NTRK1 mutations I had to reread almost ten times before it made sense. CIPA is rare, recessive, and means someone is born unable to feel pain or sweat. The gene behind it, NTRK1, has had hundreds of variants reported over the years, some that cause disease and some that don't, and the line between them isn't always obvious just by looking at a position in the gene.

This project asks a simple question: using only public data, can a model learn to tell pathogenic NTRK1 variants from benign ones, and can I actually trust why it's making that call?

## What I did

I pulled every NTRK1 variant linked to CIPA from ClinVar via the MyVariant.info API, along with CADD annotations (conservation scores, predicted deleteriousness, protein position, consequence type). After cleaning out variants with only "uncertain significance" or conflicting ClinVar calls, I was left with 706 labeled variants: 99 pathogenic or likely pathogenic, 607 benign or likely benign.

I trained a Random Forest classifier on this, with class weighting to handle the imbalance, then used SHAP to actually look inside the model rather than just trusting the accuracy number.

## What I found

The model reached a 0.987 ROC-AUC, with 91% precision and 84% recall on the pathogenic class. But the number that matters more to me is what SHAP showed about *why*:

- **CADD Phred and consequence severity score dominate the model's reasoning**, by a wide margin over everything else
- **Synonymous variants are a strong protective signal**, which makes biological sense, they don't change the protein
- **Stop-gained mutations are the single strongest individual pathogenic signal**, even though they're rare in the data
- **Conservation (GERP) and protein position matter, but much less than I expected.** The model is leaning more on "how disruptive is this change" than "where does it sit in the gene"

That last point is the one I didn't predict going in, and it's the kind of thing you only find by actually opening the model up instead of stopping at the accuracy score.

## Repo structure

## Running it

The data fetch runs anywhere with Python and `requests`:

```bash
python3 src/fetch_variants.py
```

The modeling and SHAP steps are in the notebook. I ran mine in Google Colab since it comes with scikit-learn and shap preinstalled, no local environment needed.

## Data sources

- Variant and ClinVar data: [MyVariant.info](https://myvariant.info)
- Annotations: CADD, via MyVariant.info
- The paper that started this: Wang et al. 2018, *Gene*, "Identification of a novel mutation of the NTRK1 gene in patients with congenital insensitivity to pain with anhidrosis (CIPA)"

## What's next

This is the first piece of a longer CIPA series I'm working through, variants first, then cell type mapping, since single cell analysis is where my background actually is.

---
Iqra Nadeem | [LinkedIn](https://linkedin.com/in/iqra-nadeem) | [GitHub](https://github.com/Bioinformatician0507)
