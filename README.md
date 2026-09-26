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