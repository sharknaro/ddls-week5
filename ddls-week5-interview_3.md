# DDLS 2026 — Week 5 interview transcript

**Lab:** Interview a Single-Cell Data Owner
**Data owner:** Alex Rios — PhD student who thinks they've found a novel immune cell population
**Student:** Baris Kara <baris51519@gmail.com>
**Exported:** 2026-09-23T12:38:17+00:00

> This is the record of your interview with the data owner. Hand it to your analyst agent as the raw source for `AGENTS.md` and `spec.md`.

---

**You**:

Hi Alex Rios, can you tell me about your project and elaborate what is your goal with the clustering  of the first PBMC single-cell dataset?

**Alex Rios**:

I’m Alex Rios, and this is my first PBMC single-cell dataset: 2,700 cells grouped into numbered clusters 0–7. **Cluster 4**, with about 163 cells, sits off as its own distinct group, and I can’t place it—I’m wondering if it might be a rare or novel population. My goal is to work out whether that separation reflects a genuinely new population rather than something familiar I haven’t recognized. Can you help me assess that?

**You**:

I can try. Can you provide more insight. 1) How did you obtain the data? 2) How did you notice this population? 3) How is the data collected? 4) What is the current data format? 5) What makes this particular cluster interesting for you? 6) What is your hypothesis? 7) What would you use this information once you know 8) How confident are you in your clustering interpretation in a quantitative scale?

**Alex Rios**:

1. **How obtained:** I have 2,700 PBMC single-cell measurements, but I don’t have the donor or processing details in the summary I’m looking at.

2. **How I noticed it:** After clustering and plotting the cells in 2-D, cluster 4 appeared as a distinct group of **163 cells** rather than part of the larger groups.

3. **How collected:** I can’t give you the experimental collection protocol from this summary—those metadata aren’t attached here.

4. **Current format:** Numbered clusters 0–7, with cell counts, genes detected per cell, mitochondrial-read percentages, and a 2-D map. For cluster 4, the summary says **1,263 genes/cell** and **2.4% mito**.

5. **Why interesting:** It **sits off on its own**, and I don’t recognize it from the map. That made me wonder about a rare population.

6. **Hypothesis:** My hopeful hypothesis is that cluster 4 represents **a new population**, but I haven’t established that its gene pattern is distinct from known cells.

7. **Use:** If it held up, I’d want to discuss it with my PI and design a follow-up experiment. I’m probably getting ahead of myself there.

8. **Confidence:** About **4/10** that it is genuinely novel; maybe **7/10** that it is a reproducible separated group in this analysis. Separation alone isn’t enough, right? The next thing is whether its strongest genes distinguish it from the neighboring clusters.

**You**:

1) Can you elaborate what "sits off on its own" mean in biological terms? i.e., what does this refer to in your interpretation? 2) 1) Can you elaborate what "new population" mean in biological terms? i.e., what does this refer to in your interpretation? 3) Can you elarborate what "follow-up experiments" would be and what future implications this finding might have? 4) What would be a clear and believable threshold by you and your PI, which I can use to validate if your hypothesis is true?

**Alex Rios**:

Okay, fair—**“it’s separate” isn’t the same as “it’s new,” is it?** I got ahead of myself. Biologically, “sits off on its own” only means the cells have similar measured profiles to one another and differ from other cells in the 2-D representation; it doesn’t identify what they are.

By **“new population,”** I mean a reproducible group with a coherent gene pattern that is clearly distinct from known populations—not just an isolated region of the plot. I was imagining confirming it in an independent sample and then testing whether it can be identified experimentally, but I haven’t designed that work yet.

I wouldn’t use a single numerical cutoff with my PI. A believable threshold would be: the strongest genes must distinguish cluster 4 from neighboring clusters, the pattern must not be explained by its **1,263 genes/cell** and **2.4% mito**, and the group should recur in an independent dataset or replicate. Would you treat that as enough evidence to put it on a cautious follow-up list, or would you require experimental confirmation first?

**You**:

Can you elaborate your knowledge and expectations from cluster 4 - 1) what might be the strongest marker genes, and what known immune populations do they normally indicate? 2) Does cluster 4 co-express markers from two different lineages, suggesting 3) How do its counts, detected genes, and mitochondrial percentage compare with the neighboring clusters—not just their absolute values? 4) Does cluster 4 recur across biological samples/donors, rather than being driven by one sample or batch?

**Alex Rios**:

I can’t answer the gene-specific parts from the summary I have: the strongest genes for cluster 4 aren’t included, so I can’t identify its usual immune population or test whether it co-expresses programs from two lineages. I also don’t have donor or batch labels, so recurrence across samples is unknown.

The available comparison is:

| Cluster | Cells | Genes/cell | % mito |
|---|---:|---:|---:|
| 0 | 1,197 | 809 | 1.8 |
| 1 | 489 | 850 | 2.3 |
| 2 | 445 | 828 | 2.3 |
| 3 | 347 | 673 | 2.1 |
| **4** | **163** | **1,263** | **2.4** |
| 5 | 36 | 1,570 | 2.0 |
| 6 | 13 | 350 | 1.6 |
| 7 | 10 | 2,363 | 2.0 |

So cluster 4 has 163 cells, 1,263 genes/cell, and 2.4% mitochondrial reads. It has more detected genes per cell than clusters 0–3, 6, and 7, and fewer than clusters 5 and 7; its mitochondrial percentage is 0.1–0.6 percentage points above clusters 0–3 and 0.4 above clusters 5–7. That makes the gene pattern especially important—I don’t want to call it novel from separation and these summary values alone.

Can you provide the ranked strongest genes for cluster 4, their expression in the other clusters, and the sample/batch composition?

**You**:

I will answer your question shortly. Can you elaborate - 1) Is your main question "is this a real population?", "what cell type is it?", "is it novel?", or all three? 2) Is this one donor/sample or multiple donors or conditions? 3) What exactly is the biological sample — PBMCs from whom or from what experimental condition? 4) Were the cells stimulated, treated, diseased, or otherwise different from ordinary PBMCs? 4) Roughly how many cells were originally captured?

**Alex Rios**:

1. **All three**, but in order: is it a real, coherent group; what known cell type it resembles; and only then whether it’s novel. The immediate decision is whether cluster 7—or perhaps you mean cluster 4—is worth follow-up; I’ve been focused on cluster 4, the 163-cell group.

2. Donor/sample count isn’t available in my summary.

3. The only biological description I have is PBMCs; donor identity and experimental condition aren’t attached.

4. I don’t know whether the cells were stimulated, treated, diseased, or ordinary resting PBMCs.

5. The current dataset contains **2,700 cells**. I don’t know how many were originally captured before filtering.

**You**:

Can you walk me through what is stored in the file?

**Alex Rios**:

What I can see is a **cluster summary**, not the raw experiment file. It contains:

- Cluster labels **0–7**
- Cell counts
- Mean genes detected per cell
- Mean mitochondrial-read percentage
- A 2-D cluster map

The summary values are: cluster 0, 1,197 cells/809 genes/1.8% mito; 1, 489/850/2.3%; 2, 445/828/2.3%; 3, 347/673/2.1%; 4, 163/1,263/2.4%; 5, 36/1,570/2.0%; 6, 13/350/1.6%; and 7, 10/2,363/2.0%.

I don’t have the ranked genes, per-cell expression matrix, donor or batch labels, treatment metadata, or pre-filter capture count in what I’m looking at. That’s why I can’t yet tell whether cluster 4 is biologically distinct—or whether cluster 7 is worth sending to Maya.

**You**:

Who is Maya? What is her role in this project? What is her knowledge area?

**Alex Rios**:

Maya is the person I’d send a candidate cluster to for a **follow-up experiment**—probably the wet-lab side of the project. I haven’t specified her exact role or expertise, so I shouldn’t invent that; the important point is that she would act on my label when ordering reagents. That’s why I need a conservative call on **cluster 7**, not just an interesting-looking map.

**You**:

So you are interested in cluster 4 to discuss with your PI and cluster 7 to discuss with Maya - am I correct?

**Alex Rios**:

Yes—**cluster 4** is the group I initially got excited about and would discuss with my PI. **Cluster 7** is the separate, much smaller group that needs a yes-or-no decision about sending it to Maya for follow-up. I don’t yet have enough evidence to recommend cluster 7; its summary is 10 cells, 2,363 genes/cell, and 2.0% mito, so the strongest genes and sample structure matter.

**You**:

Great then can you give me a summary of what is cluster 4 and 7? what is their importance? and what is the preferred outcome form my analysis for cluster 4 and 7 for you to proceed with your next steps?

**Alex Rios**:

**Cluster 4:** 163 cells, 1,263 genes/cell, 2.4% mito. It’s the group I first noticed because it forms its own region, but I don’t yet know its biological identity or whether it is novel. Its importance is mainly as a plausible candidate for a real, moderately sized population—provided its strongest genes separate it from known neighboring groups.

**Cluster 7:** 10 cells, 2,363 genes/cell, 2.0% mito. It is much smaller and has the highest genes-per-cell value in the summary, so I’m especially cautious about treating it as a rare discovery. Its importance is the practical decision: whether it is sufficiently credible to send to Maya for follow-up or whether we set it aside.

For cluster 4, the preferred outcome is a clear comparison of its strongest genes with the other clusters, plus evidence that it recurs across samples. For cluster 7, I need a conservative yes-or-no call: send it to Maya only if its genes form a coherent, distinct pattern that isn’t simply explained by unusually high detected-gene counts or one sample. Without those checks, I’d rather set it aside than order reagents for an artefact.

**You**:

Are you also interested in cluster 5? why/why not?

**Alex Rios**:

Not primarily. Cluster 5 has only **36 cells**, with **1,570 genes/cell** and **2.0% mito**; I’m focused on cluster 4 and the decision about cluster 7. I wouldn’t dismiss cluster 5, but I’d need its strongest genes and sample distribution before treating it as a biological population rather than another small, unusual group.

**You**:

What known immune-cell populations have you already considered as possible identities? Are there unexpected marker genes driving your interest?

**Alex Rios**:

Honestly, I haven’t assigned cluster 4 to any known immune-cell population yet—I don’t have its gene list in the summary. No unexpected genes are driving the interest; it was mainly the fact that **it sits apart on the map**, which isn’t enough to call it new. The ranked genes are what would decide this.

**You**:

Can you elaborate how you defined "sits apart on the map"? Based on what you defined this? Distance from other clusters? Also can you specify how the clustering and data processing was done

**Alex Rios**:

By **“sits apart,”** I meant visual separation in the 2-D plot—cluster 4 appeared as its own region rather than intermingled with the larger groups. I did not calculate a formal distance from other clusters, and I don’t know the exact dimensionality-reduction, normalization, or clustering settings used.

So I can’t reliably specify the processing pipeline from the file summary. What I have is the resulting numbered clusters and their summary statistics, not the code or per-cell matrix.

**You**:

Regarding your question -provide the ranked    strongest genes for cluster 4, their expression in the other clusters, and the sample/batch composition?  - There is no sample ID, donor ID, batch, library, condition, or experiment column in the         supplied .h5ad file. Therefore, sample/batch composition cannot be directly calculated from  this dataset.  Consequently, it is not possible to determine whether cluster 4 is evenly distributed across    samples or driven by a particular batch. That would require metadata such as sample, donor,     batch, or library_id.

**Alex Rios**:

Right, so **recurrence across donors or batches is unknowable from this file**. That means I can’t use cluster 4’s apparent separation as evidence that it is reproducible; I’d need the ranked genes and expression comparisons next. Do you have the top genes for cluster 4 and their values across clusters?

**You**:

the most specific cluster 4 markeers include lst1,fcer1g,fcrg3a,aif1,serpina1,ctss,cd68,cst3, and yes I have values across clusters

**Alex Rios**:

That list is useful, but I need the **cross-cluster values** before I can judge whether those genes are specific to cluster 4 or shared broadly. Please send the table for clusters 0–7—ideally expression prevalence as well as average expression.

**You**:

ank │ Gene          │ C0   │ C1   │ C2   │ C3   │ C4   │ C5   │ C6   │ C7   │                ├──────┼───────────────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤                │ 1    │ LST1          │ 0.27 │ 2.90 │ 0.24 │ 0.24 │ 3.83 │ 2.23 │ 0.24 │ 0.46 │                ├──────┼───────────────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤                │ 2    │ FCER1G        │ 0.17 │ 2.72 │ 0.93 │ 0.12 │ 3.61 │ 2.38 │ 0.70 │ 0.39 │                ├──────┼───────────────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤                │ 3    │ FCGR3A        │ 0.07 │ 0.23 │ 1.10 │ 0.06 │ 2.87 │ 0.18 │ 0.22 │ 0.31 │                ├──────┼───────────────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤                │ 4    │ COTL1         │ 1.14 │ 3.02 │ 0.74 │ 0.94 │ 3.73 │ 2.78 │ 2.19 │ 2.64 │                ├──────┼───────────────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤                │ 5    │ AIF1          │ 0.40 │ 3.03 │ 0.18 │ 0.15 │ 3.68 │ 2.10 │ 0.42 │ 0.55 │                ├──────┼───────────────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤                │ 6    │ IFITM2        │ 1.46 │ 1.53 │ 2.01 │ 1.24 │ 3.43 │ 2.07 │ 0.71 │ 1.35 │                ├──────┼───────────────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤                │ 7    │ IFITM3        │ 0.09 │ 1.46 │ 0.19 │ 0.07 │ 2.65 │ 1.16 │ 0.09 │ 0.00 │                ├──────┼───────────────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤                │ 8    │ FTH1          │ 3.17 │ 5.33 │ 3.03 │ 3.30 │ 5.62 │ 4.47 │ 4.58 │ 3.19 │                ├──────┼───────────────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤                │ 9    │ SAT1          │ 0.85 │ 3.06 │ 0.91 │ 1.14 │ 3.58 │ 2.32 │ 3.63 │ 1.30 │                ├──────┼───────────────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤                │ 10   │ SERPINA1      │ 0.12 │ 1.56 │ 0.11 │ 0.11 │ 2.32 │ 0.58 │ 0.29 │ 0.07 │                ├──────┼───────────────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤                │ 11   │ FTL           │ 3.10 │ 5.81 │ 3.18 │ 3.49 │ 5.88 │ 4.16 │ 4.17 │ 3.00 │                ├──────┼───────────────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤                │ 12   │ PSAP          │ 0.62 │ 2.60 │ 0.77 │ 0.68 │ 3.02 │ 1.79 │ 0.93 │ 0.80 │                ├──────┼───────────────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤                │ 13   │ CTSS          │ 0.62 │ 2.87 │ 0.60 │ 1.09 │ 3.21 │ 1.77 │ 0.41 │ 0.39 │                ├──────┼───────────────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤                │ 14   │ S100A11       │ 0.82 │ 2.75 │ 0.96 │ 0.23 │ 3.15 │ 2.29 │ 0.22 │ 0.76 │                ├──────┼───────────────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤                │ 15   │ OAZ1          │ 2.04 │ 3.64 │ 2.26 │ 2.53 │ 3.82 │ 3.17 │ 4.73 │ 2.76 │                ├──────┼───────────────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤                │ 16   │ RP11-290F20.3 │ 0.02 │ 0.52 │ 0.01 │ 0.03 │ 1.64 │ 0.14 │ 0.11 │ 0.00 │                ├──────┼───────────────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤                │ 17   │ CD68          │ 0.06 │ 1.55 │ 0.07 │ 0.09 │ 2.05 │ 0.67 │ 0.99 │ 0.12 │                ├──────┼───────────────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤                │ 18   │ S100A4        │ 2.19 │ 4.13 │ 3.04 │ 0.74 │ 4.23 │ 3.20 │ 0.86 │ 1.82 │                ├──────┼───────────────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤                │ 19   │ TIMP1         │ 0.45 │ 1.34 │ 0.34 │ 0.09 │ 2.35 │ 1.19 │ 2.46 │ 0.10 │                ├──────┼───────────────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤                │ 20   │ CST3          │ 0.32 │ 3.91 │ 0.38 │ 0.33 │ 3.83 │ 4.29 │ 1.94 │ 0.45 │                └──────┴───────────────┴──────┴──────┴──────┴──────┴──────┴

**Alex Rios**:

This makes cluster 4 look **coherent, but not obviously novel**. Its strongest genes—**LST1, FCER1G, FCGR3A, AIF1, CTSS, CD68, and CST3**—form a consistent immune/myeloid-associated pattern, and cluster 4 has high values for most of them.

The important comparison is that cluster 4 is not isolated at the gene level: cluster 1 is also high for LST1, FCER1G, AIF1, CTSS, and CST3, while cluster 5 shares several of these genes. Cluster 4 is particularly high for FCGR3A and SERPINA1 relative to most clusters, but the pattern is still related to existing groups rather than a completely unprecedented program. Its **1,263 genes/cell** is higher than clusters 0–3, 6, and 7, while its **2.4% mito** is close to the other clusters.

So my updated view is: cluster 4 is a credible distinct grouping worth investigating, but these results do **not** confirm a new population. The missing piece is whether its cells have a consistent profile individually and whether it recurs across samples. For the Maya decision, can you provide the corresponding strongest-gene table for cluster 7?

**You**:

─────┬───────────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┐                    │ Rank │ Gene      │ C0   │ C1   │ C2   │ C3   │ C4   │ C5   │ C6   │ C7   │                    ├──────┼───────────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤                    │ 1    │ ACTG1     │ 2.26 │ 2.38 │ 2.58 │ 1.73 │ 2.70 │ 3.14 │ 3.28 │ 4.00 │                    ├──────┼───────────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤                    │ 2    │ CFL1      │ 2.41 │ 2.61 │ 2.81 │ 1.88 │ 3.00 │ 3.04 │ 2.69 │ 3.69 │                    ├──────┼───────────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤                    │ 3    │ GAPDH     │ 2.02 │ 3.16 │ 2.44 │ 1.33 │ 2.69 │ 3.16 │ 3.15 │ 4.12 │                    ├──────┼───────────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤                    │ 4    │ KIAA0101  │ 0.00 │ 0.01 │ 0.00 │ 0.01 │ 0.01 │ 0.00 │ 0.00 │ 1.52 │                    ├──────┼───────────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤                    │ 5    │ SLC25A5   │ 0.83 │ 1.47 │ 0.84 │ 0.84 │ 1.62 │ 1.63 │ 0.38 │ 2.69 │                    ├──────┼───────────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤                    │ 6    │ STMN1     │ 0.12 │ 0.02 │ 0.25 │ 0.15 │ 0.04 │ 0.20 │ 0.12 │ 2.52 │                    ├──────┼───────────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤                    │ 7    │ ACTB      │ 3.70 │ 4.41 │ 4.25 │ 3.48 │ 4.79 │ 4.68 │ 5.68 │ 5.10 │                    ├──────┼───────────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤                    │ 8    │ FABP5     │ 0.05 │ 0.05 │ 0.03 │ 0.06 │ 0.09 │ 0.34 │ 0.00 │ 1.30 │                    ├──────┼───────────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤                    │ 9    │ H2AFV     │ 0.45 │ 0.49 │ 0.49 │ 0.23 │ 0.51 │ 0.77 │ 0.59 │ 2.00 │                    ├──────┼───────────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤                    │ 10   │ PFN1      │ 2.57 │ 3.05 │ 3.27 │ 2.15 │ 3.53 │ 3.33 │ 2.61 │ 3.95 │                    ├──────┼───────────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤                    │ 11   │ TUBB      │ 0.56 │ 0.42 │ 0.69 │ 0.51 │ 0.67 │ 0.72 │ 0.68 │ 2.51 │                    ├──────┼───────────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤                    │ 12   │ PCNA      │ 0.12 │ 0.04 │ 0.14 │ 0.07 │ 0.11 │ 0.13 │ 0.12 │ 1.53 │                    ├──────┼───────────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤                    │ 13   │ SNRPB     │ 0.57 │ 0.47 │ 0.79 │ 0.64 │ 0.72 │ 0.97 │ 0.26 │ 2.05 │                    ├──────┼───────────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤                    │ 14   │ HMGB2     │ 0.55 │ 0.85 │ 0.56 │ 0.39 │ 0.53 │ 0.66 │ 0.52 │ 2.78 │                    ├──────┼───────────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤                    │ 15   │ CCT5      │ 0.27 │ 0.26 │ 0.33 │ 0.27 │ 0.68 │ 0.56 │ 0.06 │ 1.62 │                    ├──────┼───────────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤                    │ 16   │ HMGB1     │ 1.35 │ 0.95 │ 1.50 │ 1.46 │ 1.10 │ 1.20 │ 2.59 │ 2.95 │                    ├──────┼───────────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤                    │ 17   │ SRSF3     │ 0.90 │ 0.88 │ 1.10 │ 0.72 │ 0.81 │ 1.24 │ 0.19 │ 2.35 │                    ├──────┼───────────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤                    │ 18   │ ATP5B     │ 0.65 │ 0.87 │ 0.75 │ 0.56 │ 1.30 │ 1.43 │ 0.65 │ 2.17 │                    ├──────┼───────────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤                    │ 19   │ TYMS      │ 0.00 │ 0.00 │ 0.01 │ 0.01 │ 0.01 │ 0.03 │ 0.00 │ 1.52 │                    ├──────┼───────────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤                    │ 20   │ HNRNPA2B1 │ 1.34 │ 0.90 │ 1.52 │ 1.45 │ 1.37 │ 1.78 │ 1.09 │ 2.78 │                    └──────┴───────────┴──────┴──────┴──────┴──────┴──────┴──────

**Alex Rios**:

**No—I would not send cluster 7 to Maya.** Its 10 cells have **2,363 genes/cell** and **2.0% mito**, but the strongest genes are mostly broadly expressed or replication-associated: **KIAA0101, STMN1, PCNA, TYMS, HMGB2, SNRPB, and H2AFV**. They are elevated in cluster 7, but I don’t see a coherent lineage-specific gene pattern in this table.

Compared with cluster 4, cluster 7 is not supported by genes such as LST1, FCER1G, FCGR3A, or AIF1; its apparent distinctness seems much more tied to unusually high gene detection and a proliferation-related signal. Given the tiny size and absent sample metadata, I’d **set cluster 7 aside as an artefact/low-confidence lead**, rather than order reagents for it.

**You**:

what result would make cluster 4 known-cell follow-up rather than a novel-population claim. Can you elarboate what is the coherence of cluseter 7 markers in comparison to the other clusters? How should I approach the per-cell consistency and potential doublets or mixed-lineage artefact that is not accessed for cluster 4 and 7?

**Alex Rios**:

For **cluster 4**, a result supporting a known-cell follow-up would be: its cells consistently express the same myeloid-associated genes—especially **LST1, FCER1G, FCGR3A, AIF1, CTSS, CD68, and CST3**—and those genes are shared with an established neighboring cluster rather than forming a unique program. If the pattern is consistent per cell, without a second incompatible lineage, I’d label it as a known population and drop the novel-population claim.

For **cluster 7**, the top genes are coherent mainly as a high-activity/proliferation-like signal: **STMN1, PCNA, TYMS, KIAA0101, HMGB2, SNRPB**, and related genes are elevated relative to the other clusters. But they do not form a clear lineage identity, and genes such as ACTG1, GAPDH, ACTB, CFL1, and PFN1 are broadly expressed. With only 10 cells and **2,363 genes/cell**, I’d regard that as weak biological coherence, not evidence of a new cell type.

For the per-cell check, I’d look at whether the putative cluster-4 genes occur together across most of its 163 cells, rather than being driven by a few cells. I’d also inspect each cell for simultaneous strong programs from incompatible lineages; that would raise concern about mixed cells or doublets. The same check is especially important for cluster 7: determine whether all 10 cells share the pattern or whether one or two unusually gene-rich cells are driving the cluster. The current averages cannot answer that.

My practical call remains: **cluster 4 gets a cautious known-cell characterization first; cluster 7 stays off Maya’s list** unless the per-cell inspection shows a reproducible, lineage-specific pattern. Do you have per-cell expression or only these cluster-level averages?

**You**:

We are working on your request, in the mean time can you give clear definition of What would a convincing final answer look like to you? What result would make the analysis misleading or unusable for you? How should we validate that the navigator and calculated numbers are correct?

**Alex Rios**:

A convincing final answer would be an explicit call for each cluster, tied to the data:

- **Cluster 4:** whether it is a coherent known population, a possible novel population, or unresolved. I’d want that based on per-cell consistency of its myeloid-associated genes—**LST1, FCER1G, FCGR3A, AIF1, CTSS, CD68, CST3**—comparison with neighboring clusters, and checks for mixed-lineage cells. With the current table, “known myeloid-like population; novelty not supported” is more defensible than a novel-population claim.
- **Cluster 7:** a yes/no decision on Maya. Given **10 cells**, **2,363 genes/cell**, and top genes dominated by **STMN1, PCNA, TYMS, KIAA0101, HMGB2** plus broadly expressed genes, a convincing answer is **do not send it for follow-up** unless per-cell data overturn that interpretation.

The analysis would be misleading or unusable if it called either cluster novel from the 2-D separation alone, treated cluster-average expression as if every cell had the same profile, ignored the very different cluster sizes, or presented donor/batch recurrence as established when the file has no such metadata. For cluster 7 specifically, I’d consider the result unusable for experimental planning if its apparent signal comes from only one or two cells, or if the cells show incompatible lineage programs consistent with mixed cells.

For validation, I’d first reconcile the reported cell counts with the 2,700-cell total and verify that the cluster labels, `n_genes`, and `pct_mito` values were calculated from the same filtered matrix. Then I’d independently recompute the cluster-level means from the per-cell matrix, inspect distributions rather than only averages, and confirm that the displayed ranked genes and values correspond to the stated cluster labels. I’d also verify that the 2-D plot uses those same labels and cells—not a different filtering or clustering run.

One limitation cannot be fixed computationally here: without donor, sample, or batch metadata, reproducibility across biological samples cannot be validated. That needs the original annotations or an independent dataset.

**You**:

Regarding your per-cell expression question - what would you like to know?

**Alex Rios**:

For **cluster 4**, I’d like, for each of the 163 cells:

- `n_genes` and `pct_mito`
- Whether each cell expresses the main genes **LST1, FCER1G, FCGR3A, AIF1, CTSS, CD68, CST3**
- Whether those genes occur together in most cells or are driven by a subset
- Any strong genes from a clearly different lineage in the same cells

For **cluster 7**, the same information for all 10 cells, especially **STMN1, PCNA, TYMS, KIAA0101, HMGB2**, plus whether the unusually high `n_genes` is shared across all 10 or concentrated in one or two cells. If you have a per-cell doublet or mixed-profile flag, include that too—but the expression pattern itself is the key check.

A compact table with one row per cell and columns for cluster, `n_genes`, `pct_mito`, and those genes’ expression—or at least detection yes/no—would be enough. Can you also tell me whether the values are raw counts, normalized values, or log-transformed values?

**You**:

Can you confirm that cluster 4 is a cautious known-myeloid follow-up candidate, while cluster 7 should stay off Maya`s list absent contrary per-cell evidence?

**Alex Rios**:

I wouldn’t call it **confirmed** yet—that’s what the per-cell check is for. Based on the current cluster-level data, cluster 4 is a cautious follow-up candidate with a known myeloid-like pattern, while cluster 7 should stay off Maya’s list provisionally; you tell me whether the cell-level evidence supports or overturns that call.

**You**:

I cannot provide you the compact table, what would be the most compact short information I can share with you to confirm?

**Alex Rios**:

The shortest useful summary would be, for each cluster:

```text
Cluster 4 (n=163):
median [range] n_genes:
median [range] pct_mito:
cells expressing ≥1 count of LST1+FCER1G+FCGR3A+AIF1+CTSS+CD68+CST3:
cells co-expressing at least 3 of those genes:
cells with strong non-myeloid markers:
doublet-flagged cells:

Cluster 7 (n=10):
median [range] n_genes:
median [range] pct_mito:
cells expressing STMN1, PCNA, TYMS, KIAA0101:
cells co-expressing at least 3 of those genes:
cells with a recognizable lineage pattern:
doublet-flagged cells:
```

Please state whether “expressing” means detected above zero, and whether the values are raw or normalized. That would support or weaken the provisional call, though it still wouldn’t establish donor-level recurrence.

**You**:

Cluster 4 (n=163):                                                                              median [range] n_genes: 1263 [390–1938]                                                         median [range] pct_mito: 2.41% [0.13–22.57%]                                                    cells expressing ≥1 count of LST1+FCER1G+FCGR3A+AIF1+CTSS+CD68+CST3: 163/163 (100%)             cells co-expressing at least 3 of those genes: 163/163 (100%)                                   cells with strong non-myeloid markers: 112/163 (68.7%); this flag includes cells expressing     at least one of CD3D, CD3E, MS4A1, CD79A, NKG7, GNLY, CCL5, GZMB, PPBP, or PF4. This is         likely a permissive contamination/ambient-RNA screen rather than definitive evidence of         doublets.                                                                                       doublet-flagged cells: 0 official flags; no doublet scores were included. One cell exceeded     5% mitochondrial content, and none exceeded 2,500 detected genes.                                                                                                                               Cluster 7 (n=10):                                                                               median [range] n_genes: 2363.5 [1597–3422]                                                      median [range] pct_mito: 2.03% [1.12–4.10%]                                                     cells expressing STMN1, PCNA, TYMS, KIAA0101: 10/10 expressed at least one of these genes       cells co-expressing at least 3 of those genes: 8/10 (80%)                                       cells with a recognizable lineage pattern: 10/10 show mixed lymphoid/cytotoxic and              proliferative features; 7 express CD3D/CD3E, 8 express NKG7, 7 express CCL5, and 7 express      MKI67. This appears more consistent with a small cycling lymphoid/cytotoxic population than a   clean, single-lineage cluster.                                                                  doublet-flagged cells: 0 official flags; no doublet scores were included. However, 5/10 cells    exceeded 2,500 detected genes and should be reviewed as possible high-complexity cells or      potential doublets.

**Alex Rios**:

This changes the call slightly:

- **Cluster 4:** I would call it a **myeloid-like follow-up candidate, not a confirmed clean known population**. The strongest evidence is that all 163 cells express at least three of the myeloid-associated genes. But 112/163 also trigger the permissive non-myeloid screen, and there are no doublet scores, so I would not make a novelty claim—or treat the cluster as experimentally ready—until those cells are reviewed individually. The one cell at **22.57% mito** also deserves separate scrutiny.

- **Cluster 7:** **Keep it off Maya’s list.** Eight of ten co-express the proliferation-associated genes, but all ten are described as mixed lymphoid/cytotoxic and proliferative, and five have more than 2,500 detected genes. With only 10 cells and no doublet assessment, that is not a reliable single-lineage population.

So the practical decision is: **cluster 4 gets cautious internal follow-up; cluster 7 is set aside.** For cluster 4, the most useful next compact result would be the number of cells co-expressing the myeloid program *without* any strong lymphoid/cytotoxic or platelet program, rather than the permissive “at least one marker” count.

**You**:

Yes.                                                                                                                                                                                            - “Expressing” means detected above zero raw counts in adata.layers["counts"].                      - A cell is counted as expressing a gene when its raw UMI count is > 0.                         - Thus, “cells expressing ≥1 count” is a binary detection criterion, not a minimum                normalized-expression threshold.                                                                                                                                                          - The reported expression values in the earlier gene-expression tables are from adata.X.            - adata.X contains log-normalized expression values, not raw counts.                            - These values are appropriate for comparing relative expression levels across cells or           clusters, but they are not UMI counts.                                                                                                                                                    - n_genes and pct_mito are QC metadata derived from the count data:                                 - n_genes: number of genes with detected counts                                                 - pct_mito: percentage of total counts attributed to mitochondrial genes                                                                                                                    Therefore:                                                                                                                                                                                      - The statement that all 163 cluster 4 cells express at least one of the specified myeloid        markers is based on raw-count detection.                                                      - The statement that all 163 co-express at least three markers is also based on raw counts        greater than zero.                                                                            - These observations support the provisional cluster 4 myeloid/monocyte assignment because        the signal is broadly detected across cells, rather than appearing only as isolated             normalized-expression outliers.                                                               - However, this does not establish recurrence across donors or samples because the file           contains no donor, sample, library, or batch identifiers.

**Alex Rios**:

That supports the provisional call: **cluster 4 is a credible myeloid/monocyte-like follow-up candidate**, because the program is detected across all 163 cells in raw counts, not just a few high normalized-expression cells. It still does **not** support a novel-population claim: the non-myeloid screen affects 112 cells, donor recurrence is unavailable, and there are no formal doublet scores.

I’d report it as: “Cluster 4 shows a broadly consistent myeloid program and warrants cautious known-cell follow-up; novelty remains unestablished.” Cluster 7 stays off Maya’s list. The remaining useful check for cluster 4 is whether those 112 flagged cells show a coherent second program or merely isolated low-level detections.

**You**:

Can you answer 1) When we say a gene is “expressed,” should we define that as raw count > 0, or use a threshold on normalized/log-transformed expression? 2)For the marker tables I gave you, do you want the interpretation based on raw counts, normalized expression, or log-transformed expression? 3) If the .h5ad contains a doublet score/flag, what level of doublet evidence would materially change your decision for clusters 4 or 7? 4) For cluster 4, what minimum per-cell consistency would you regard as convincing—for example, should most cells co-express at least 3 of the 7 myeloid-associated markers? 4) For cluster 7, what observation would overturn your current “do not send to Maya” position?

**Alex Rios**:

1. Use **raw count > 0** for a binary detection statement, and state that explicitly. For stronger claims about marker enrichment, use normalized/log-transformed values or detection fractions with a defined threshold; don’t treat any nonzero count as strong expression.

2. For the marker tables, interpret the reported values as **log-normalized expression from `adata.X`**, suitable for comparing relative expression across clusters. Use the raw-count layer separately to report how many individual cells detect each gene. So: normalized values for ranking/enrichment, raw counts for per-cell detection and co-expression.

3. There isn’t a universal doublet-score cutoff I’d trust without seeing the score distribution. It would materially change my call if:
   - a large fraction of cluster 4 had scores clearly in the dataset’s high-score tail, especially alongside two strong incompatible lineage programs; or
   - most or all of cluster 7 had high doublet scores and high gene counts.

   A few flagged cells would not invalidate cluster 4; I’d remove or review them. For cluster 7, even moderate evidence across several of its 10 cells would reinforce keeping it off Maya’s list.

4. For cluster 4, **most cells co-expressing at least 3 of the 7 genes** would be a reasonable minimum for a provisional coherent program—roughly 80–90% would convince me more than a simple majority. You already report 163/163, so that criterion is met. The remaining concern is whether the 112 cells with non-myeloid detections have a genuine second program or only isolated low-level counts.

5. Cluster 7 would overturn my “do not send” position only if the per-cell data showed a reproducible, coherent identity across nearly all 10 cells: the same lineage-associated genes, not merely cell-cycle genes; little evidence of mixed incompatible programs; no substantial doublet-score enrichment; and no dependence on one or two exceptionally gene-rich cells. The current pattern—8/10 with at least three proliferation-associated genes, lymphoid/cytotoxic features in all 10, and 5/10 above 2,500 detected genes—doesn’t meet that bar.

**You**:

Should the final navigator explicitly label conclusions as “known-like,” “unresolved,” and “low-confidence/artifact candidate,” or would you prefer the evidence shown without categorical labels? If cluster 4 turns out to be a known myeloid subtype rather than novel, is identifying the most likely known subtype sufficient for your PI discussion? Which clusters do you consider the biologically relevant “neighbors” of cluster 4—based on the 2-D map, expression similarity, or both?

**Alex Rios**:

Use the categorical labels **with the evidence beside them**: “known-like,” “unresolved,” and “low-confidence/artifact candidate.” A label alone could be over-read, but evidence without a decision is not useful for my PI or Maya.

If cluster 4 is assigned a likely known myeloid subtype, that is sufficient for a PI discussion—provided the assignment includes its supporting genes, per-cell consistency, and the limitation that donor/batch recurrence is unavailable. I would not present it as novel unless the data show a reproducible program distinct from known groups.

For neighbors, I’d use **both**: physical proximity on the 2-D map to identify candidates, then expression similarity to determine which comparisons are biologically meaningful. From the table, cluster 1 is the clearest expression neighbor because it shares high LST1, FCER1G, AIF1, CTSS, and CST3; cluster 5 also shares part of that program, while cluster 2 is relevant for FCGR3A. The map alone shouldn’t define the comparison.

**You**:

Define "with the evidence beside them" - what would be considered as an evidence.

**Alex Rios**:

By **“evidence beside them,”** I mean the specific observations that justify the label, not just a general description. For example:

- **Known-like:** the strongest genes, their relative expression in comparison clusters, the fraction of cells detecting the key genes, and the fraction co-expressing the program.
- **Unresolved:** conflicting signals, weak or incomplete marker support, substantial variation across cells, or missing metadata that prevents a firm assignment.
- **Low-confidence/artifact candidate:** very small cell number, unusually high `n_genes`, high doublet scores, mixed incompatible programs, or a signal driven by only a few cells.

For cluster 4, that would read something like: “Known-like myeloid candidate — 163/163 cells detect at least three of seven myeloid-associated genes; its log-normalized expression is highest or near-highest for several of them; it shares the program with clusters 1 and 5; no sample metadata or formal doublet scores are available; 112/163 trigger a permissive non-myeloid screen.”

For cluster 7: “Low-confidence/artifact candidate — n=10; median 2,363.5 genes/cell; 8/10 co-express at least three proliferation-associated genes; all 10 show mixed lymphoid/cytotoxic and proliferative features; 5/10 exceed 2,500 genes; no formal doublet scores.” That is the level of evidence I’d want visible next to each label.

**You**:

Let me play back what I understand to make sure I have captured your needs correctly.  Your main goal is to determine whether the unusual clusters represent biologically coherent cell populations rather than assuming that separation on the 2-D map means novelty.  For **cluster 4**, you want me to determine its most likely biological identity and whether its myeloid-associated program is consistent across individual cells. Based on the evidence so far, it is a **known-like myeloid/monocyte follow-up candidate**, not evidence of a novel population. The conclusion should be supported by its marker genes, their expression relative to other clusters, per-cell detection and co-expression, comparison particularly with clusters 1, 5 and 2, and examination for incompatible lineage programs or possible doublets.  For **cluster 7**, the practical question is whether it is credible enough to send to Maya for experimental follow-up. Based on its very small size, high genes-per-cell, proliferation-associated markers and mixed lymphoid/cytotoxic features, the current position is **low-confidence and do not send it to Maya unless stronger per-cell evidence overturns that interpretation**.  The final navigator should therefore give a categorical interpretation such as **known-like, unresolved, or low-confidence/artifact candidate**, but always display the supporting evidence beside that label.  I should also make clear that this dataset cannot establish recurrence across donors, samples or batches because those metadata are unavailable, and there are no formal doublet scores.  **Have I understood your goal, decision criteria, and required evidence correctly? Is there anything important I have missed or anything you would change before I use this as the specification for the analysis and navigator?**

**Alex Rios**:

Yes, that captures it. I’d make one important wording change: call cluster 4 **“known-like myeloid candidate”**, not a confirmed monocyte subtype, unless the broader marker comparison supports a more specific assignment.

For the specification, keep these distinctions explicit:

- Raw counts >0 for detection/co-expression.
- Log-normalized `adata.X` for relative expression and marker comparison.
- Cluster 4: known-like, with novelty unestablished; report its 163/163 co-expression result, comparisons with clusters 1/5/2, the permissive non-myeloid flag, and absent doublet/sample metadata.
- Cluster 7: **low-confidence/artifact candidate; do not send to Maya** unless nearly all cells show a coherent lineage program, low doublet evidence, and the result is not driven by high gene counts or a few cells.
- Validate that cluster labels, cell counts, QC values, expression values, and ranked genes all come from the same matrix and filtering state.

I’d also avoid calling cluster 7 definitively an artefact: “low-confidence/artifact candidate” is the right level. That’s the specification I’d use.

**You**:

Great - finally. Can you state what would done look like with the analysis outcome of these clusters by you and the follow-up people

**Alex Rios**:

“Done” would mean the navigator gives an explicit, evidence-linked outcome:

- **Cluster 4 — known-like myeloid candidate; cautious follow-up.** Report the supporting genes, comparison with clusters 1/5/2, 163/163 cells co-expressing at least three myeloid-associated genes, the non-myeloid-screen result, and the absence of donor/batch and formal doublet information. I would discuss it with my PI as a likely known population, **not as a novel discovery**. Maya could consider follow-up only after reviewing the per-cell mixed-lineage and doublet concerns.

- **Cluster 7 — low-confidence/artifact candidate; do not send to Maya.** Record its 10-cell size, high gene counts, proliferative genes, mixed lymphoid/cytotoxic pattern, 5/10 cells above 2,500 genes, and lack of doublet scores. It stays out of experimental planning unless additional evidence shows a coherent lineage program across nearly all cells.

For me, the analysis is complete when those labels, supporting numbers, limitations, and a clear action—**cautious internal follow-up for cluster 4; set aside cluster 7**—are all visible without requiring Maya or my PI to reinterpret the whole dataset.

**You**:

Can you specify also what it the prefered final handoof format and intended auidence use - navigator layoutm evidence details, how PI/Maya decisions should be. Also elaborate,  what validation and reproducibility boundaries are required - checks, tolerances, and what constitutes a failed validation. Finally, state what is the action plan after the labels - ownership, review steps, and criteria for advancing or closing cluster 4 follow-up

**Alex Rios**:

Yes. I’d want the handoff to be a **decision-oriented navigator**, not just a plot collection.

## Preferred handoff format

### 1. One-page summary for PI and Maya

A table like:

| Cluster | Label | Evidence | Limitation | Action |
|---|---|---|---|---|
| 4 | Known-like myeloid candidate | 163 cells; 1,263 median genes/cell; 2.4% mito; 163/163 co-express ≥3 of 7 myeloid-associated genes; similarity to clusters 1, 5 and 2 | No donor/batch metadata; no formal doublet scores; 112/163 trigger a permissive non-myeloid screen | Discuss with PI; cautious internal follow-up; no novelty claim |
| 7 | Low-confidence/artifact candidate | 10 cells; 2,363.5 median genes/cell; 8/10 co-express ≥3 proliferation-associated genes; mixed lymphoid/cytotoxic features; 5/10 >2,500 genes/cell | No formal doublet scores; tiny cluster; high complexity | Do not send to Maya; set aside pending contrary evidence |

The label, supporting numbers, limitations, and action should be visible together. Maya should not have to infer the action from a map.

### 2. Evidence pages or appendix

For each cluster, include:

- cluster size and QC distributions;
- top genes and values from log-normalized `adata.X`;
- detection fractions from raw counts;
- per-cell co-expression summary;
- comparison with biologically relevant neighboring clusters;
- doublet-score information, if available;
- exact data layer and threshold definitions;
- a note stating that donor, sample, batch, and library recurrence cannot be assessed.

### 3. Technical provenance

The handoff should record:

- input `.h5ad` filename and version/date;
- cell and gene filtering;
- normalization and transformation;
- source of cluster labels;
- source of `n_genes` and `pct_mito`;
- exact marker-ranking method;
- whether values are raw counts or log-normalized values;
- software and analysis version if available.

That is mainly for the analyst and me, not for Maya, but it is what makes the result auditable.

## How PI and Maya should use it

**PI:** use the summary to decide whether cluster 4 merits a known-cell interpretation and a small validation effort. I would present it as “a coherent myeloid-like cluster whose novelty is unsupported,” not as a discovery.

**Maya:** should act only on an explicit “advance” recommendation. Cluster 7 should be marked **do not order reagents**. Cluster 4 should not trigger a novel-population experiment yet; at most, it supports targeted confirmation of the likely known identity.

## Validation and reproducibility boundaries

I’d separate validation into three levels.

### Computational consistency

Pass if:

- cluster counts sum to **2,700**;
- cluster 4 has 163 cells and cluster 7 has 10;
- reported QC summaries can be reproduced from the same count matrix;
- marker values match the stated source, `adata.X`;
- detection and co-expression results match `adata.layers["counts"]`;
- labels and expression values refer to the same filtered cells.

A mismatch in cluster membership, matrix layer, filtering state, or cell count would be a **failed validation**, not a minor caveat.

For numerical summaries, tiny differences from rounding are acceptable—for example, a displayed value differing only in the last reported decimal. A materially different median, range, detection count, or marker rank would require investigation.

### Biological coherence

For cluster 4, I’d regard the current evidence as passing the **provisional coherence** check because 163/163 cells co-express at least three of the seven genes. I would still want to know whether the non-myeloid signals are isolated low-level detections or a genuine second program.

A failed coherence check would be:

- the myeloid program is concentrated in a minority of cells;
- the cluster separates only because of QC variables;
- most cells show a strong incompatible lineage program;
- or removing a few cells eliminates the apparent distinction.

For cluster 7, it would pass only if nearly all cells shared a coherent lineage-associated program beyond proliferation, with no strong dependence on the five high-complexity cells.

### Biological reproducibility

This dataset cannot pass donor- or batch-level reproducibility because those identifiers are absent. That is a **boundary of the analysis**, not something we can infer from the cluster table.

A novel-population claim would therefore fail validation here unless it were independently reproduced in another annotated dataset or in new samples. Cluster 4 can be discussed as known-like, but not as a validated novel population.

## Action plan after labeling

### Cluster 4

**Owner:** I would own the biological interpretation and PI discussion; the analyst owns the reproducible computation and evidence package; Maya only acts after the PI agrees on the proposed confirmation.

1. Analyst supplies the navigator and technical provenance.
2. I review the per-cell mixed-lineage flags and inspect whether they are coherent secondary programs or permissive detections.
3. We apply any available doublet scoring and review high-mitochondrial or unusually high-complexity cells.
4. I present cluster 4 to the PI as a known-like myeloid candidate.
5. Advance it only if the per-cell program remains coherent after QC/doublet review and the proposed experiment tests the likely known identity.
6. Close the novelty claim unless an independent dataset shows a distinct, reproducible program.

### Cluster 7

**Owner:** I would document the rationale for setting it aside; no reagent or experiment owner is assigned yet.

1. Record the current low-confidence label.
2. Review the five high-complexity cells and any available doublet scores.
3. Reopen only if most cells show a consistent non-proliferative lineage identity, low doublet evidence, and the signal is not driven by one or two cells.
4. Otherwise close it as an experimental lead.

So the final operational outcome is: **cluster 4 advances to cautious known-cell review; cluster 7 is closed for experimental follow-up unless specific contrary evidence appears.**
