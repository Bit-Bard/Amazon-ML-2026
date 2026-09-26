Things to remember 
1. Best Feature
2. Best approach
3. Best architecture 

Step 1 
RAW DATA
   ↓
Unicode normalization
   ↓
Case + punctuation normalization
   ↓
Abbreviation normalization
   ↓
Name normalization
   ↓
Address normalization
   ↓
Number extraction
   ↓
Token extraction
   ↓
name_full_clean + name_core
   ↓
Save processed data


Step 2 


Final pipeline (10 steps)

Step        Task
1           Data Cleaning & Normalization ✅
2           BGE-M3 + TF-IDF Representation
3           FAISS Index Creation
4           Top-20 Candidate Generation
5           Candidate Union + Cheap Filtering
6           Pairwise Feature Engineering
7           Create Labels + Hard Negative Sampling
8           Stage 1: LGBM + CatBoost + XGBoost + TabM → Ridge
9           Stage 2: Residual Models → Ridge
10          Threshold Optimization → matching_results.tsv + candidate_pairs.tsv


Here is a clean, well-formatted Markdown version ready to drop straight into your GitHub `README.md`. It uses organized tables and clean code blocks for optimal rendering.

---

### 📊 Model Features (Stage 1)

These **36 engineered features** serve as the direct input to **LightGBM**, **CatBoost**, **XGBoost**, and **TabM** in Stage 1.

#### A. Semantic Features (6)

| # | Feature | Description / Formula |
| --- | --- | --- |
| 1 | `bge_cosine` | Cosine similarity from BGE embeddings |
| 2 | `tfidf_score` | TF-IDF similarity score |
| 3 | `bge_rank` | Dense retrieval rank |
| 4 | `score_gap` | Score difference relative to top candidate |
| 5 | `reciprocal_rank` | Reciprocal rank ($1 / \text{rank}$) |
| 6 | `cosine_percentile` | Percentile rank of cosine similarity score |

#### B. Name Features (10)

| # | Feature | Description |
| --- | --- | --- |
| 7 | `name_jaro` | Jaro-Winkler distance on names |
| 8 | `name_levenshtein` | Levenshtein distance on names |
| 9 | `name_jaccard` | Token Jaccard similarity on names |
| 10 | `name_token_overlap` | Exact token overlap ratio |
| 11 | `name_word_count` | Query name token count |
| 12 | `candidate_name_word_count` | Candidate name token count |
| 13 | `name_count_diff` | Difference in token length |
| 14 | `name_prefix_match` | Boolean / ratio prefix match |
| 15 | `name_suffix_match` | Boolean / ratio suffix match |
| 16 | `common_name_tokens` | Absolute count of shared name tokens |

#### C. Address Features (12)

| # | Feature | Description |
| --- | --- | --- |
| 17 | `address_jaccard` | Token Jaccard similarity on address |
| 18 | `address_levenshtein` | Levenshtein distance on address string |
| 19 | `address_token_overlap` | Token overlap ratio |
| 20 | `address_word_count` | Query address word count |
| 21 | `candidate_address_word_count` | Candidate address word count |
| 22 | `address_count_diff` | Word count difference |
| 23 | `number_overlap` | Overlap of extracted numbers |
| 24 | `building_number_match` | Exact match on building/street number |
| 25 | `pin_match` | Exact match on Postal Code / PIN |
| 26 | `city_match` | Exact match on City |
| 27 | `state_match` | Exact match on State |
| 28 | `common_address_tokens` | Count of shared address tokens |

#### D. Country & Numeric Features (4)

| # | Feature | Description |
| --- | --- | --- |
| 29 | `country_match` | Boolean match on Country |
| 30 | `numeric_jaccard` | Jaccard similarity over all extracted numbers |
| 31 | `total_numbers` | Extracted number count (Query) |
| 32 | `candidate_total_numbers` | Extracted number count (Candidate) |

#### E. Interaction Features (4)

| # | Feature | Formula / Source |
| --- | --- | --- |
| 33 | `semantic_address_interaction` | $\text{bge\_cosine} \times \text{address\_jaccard}$ |
| 34 | `semantic_tfidf_interaction` | $\text{bge\_cosine} \times \text{tfidf\_score}$ |
| 35 | `avg_similarity` | Average over primary similarity metrics |
| 36 | `max_similarity` | Peak similarity across core features |


After Step 6 Merging 

##Merging 

AmazonML/
│
├── pair_features/
│   ├── train_features_shard_0.parquet
│   ├── train_features_shard_1.parquet
│   ├── train_features_shard_2.parquet
│   ├── train_features_shard_3.parquet
│   ├── test_features_shard_0.parquet
│   ├── test_features_shard_1.parquet
│   ├── test_features_shard_2.parquet
│   └── test_features_shard_3.parquet


## this will be final dataset to train 
pair_features/
│
├── merged/
│   ├── merged_train_features.parquet
│   └── merged_test_features.parquet