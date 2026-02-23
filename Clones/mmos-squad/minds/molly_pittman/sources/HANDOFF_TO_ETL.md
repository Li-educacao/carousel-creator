# ETL Squad Handoff - Molly Pittman Cognitive Cloning
## Mind Mapper → Data Collector Delegation

**Date:** 2026-02-15
**Subject:** Parallel collection for Molly Pittman mind mapping project
**From:** Mind Mapper (MMOS orchestrator)
**To:** @data-collector (ETL Squad master orchestrator)
**Status:** Ready for parallel collection execution

---

## PROJECT CONTEXT

**Mind Name:** molly_pittman
**Viability Status:** ✅ GO (APEX: 86/100, ICP: 88%)
**Discovery Status:** ✅ COMPLETE (22 sources identified)
**Phase:** Phase 1B - Research Collection (Parallel Execution)

---

## COLLECTION SCOPE

### Source Inventory
- **Total Sources:** 22 (grouped into 3 tiers)
- **Source Types:** 5 (books, articles, interviews, courses, video)
- **Temporal Span:** 11 years (2014-2025)
- **Tier Breakdown:**
  - Tier 1 (Critical): 8 sources
  - Tier 2 (Important): 10 sources
  - Tier 3 (Nice-to-have): 4 sources

### Collection Requirements
- Minimum requirements: **EXCEED** (22/15 sources, 8/5 Tier 1)
- Quality standard: Tier 1 must be 100% collected
- Estimated success rate: >90% achievable
- Time estimate: 2-4 hours with parallelization

---

## BATCH CONFIGURATIONS

Three YAML configuration files have been prepared:

1. **tier1_batch.yaml** — Critical sources (execute immediately)
2. **tier2_batch.yaml** — Important sources (run in parallel)
3. **tier3_batch.yaml** — Secondary sources (execute if time permits)

**Path:** `squads/mmos-squad/minds/molly_pittman/sources/{tier1|tier2|tier3}_batch.yaml`

---

## SOURCE DETAILS BY TYPE

### Type 1: Books (2 sources)
- ✅ Click Happy (Molly Pittman, 2021, 45K words) — **CRITICAL**
  - URL: https://mollypittman.com/
  - Format: Ebook/Paperback
  - Priority: Highest (Layer 6-8 values)

- ✅ Co-authored book with Ryan Deiss (2014, 30K words) — **IMPORTANT**
  - URL: Amazon search
  - Format: Published
  - Priority: Context for early career

### Type 2: Blog/Articles (8 sources)
- ✅ Forbes & Entrepreneur Magazine articles (multiple) — **CRITICAL**
  - Priority: Tier 1 publications

- ✅ Blog archive - mollypittman.com (100+ posts) — **CRITICAL**
  - URL: https://mollypittman.com/blog/
  - Posts: 100+
  - Span: 2012-2025
  - Priority: Comprehensive tactical + philosophy evolution

- ✅ "5 Key Elements of the Perfect Facebook Ad" (Buffer) — **IMPORTANT**
  - URL: https://buffer.com/resources/facebook-ad-molly-pittman/

### Type 3: Interviews/Podcasts (10 sources)
**CRITICAL (Tier 1) - Recent interviews (must collect):**
- Marketing in 2025 (Parker T Nash, Dec 2024)
  - URL: https://www.parkertnash.com/podcast-14-molly-pittman-smart-marketer/

- Real Talk With Molly Pittman (Smart Marketer Podcast, Ep 105, Jun 2024)
  - URL: https://podcasts.apple.com/gb/podcast/real-talk-with-molly-pittman-fueled-by-passion-balance/id1522629407?i=1000570291548
  - Note: **CORE values interview**

- The Paid Traffic Tectonic Shift (Marketing Speak, Feb 2025)
  - URL: https://www.marketingspeak.com/the-paid-traffic-tectonic-shift-with-molly-pittman/

- Perpetual Traffic Podcast Archive (Co-host, 100+ episodes)
  - URL: https://perpetualtraffic.com/
  - **GOLDMINE**: Authentic voice, daily decision patterns
  - Priority: Collect last 50 episodes minimum

**IMPORTANT (Tier 1-2) - Career interviews:**
- How To Win On Social Media (James Schramko, 2019)
- Molly Pittman - Facebook Ads Phenom (Wild Business Growth, 2020)
- How To Train a Media Buyer (Alex Fedotoff, 2020)
- Reverse Interview (Chris Harder, 2021)

### Type 4: Courses & Training (1 source)
- ✅ Smart Marketer Curriculum & Certifications — **IMPORTANT**
  - URL: https://smartmarketer.com/
  - Type: Online course platform
  - Collection: Course outlines, free samples, student testimonials
  - Contains: Proprietary frameworks (Layer 5 mental models)

### Type 5: Video (1 source)
- ✅ Smart Marketer YouTube Channel (@thesmartmarketer) — **IMPORTANT**
  - URL: https://www.youtube.com/@thesmartmarketer
  - Videos: 50+
  - Strategy: Last 20 videos + transcripts

---

## SPECIALIST AGENT ROUTING

Route sources as follows:

| Source Type | Specialist Agent | Sources |
|------------|-----------------|---------|
| **Books** | @document-specialist | Click Happy, Co-authored book |
| **Blog/Articles** | @web-specialist | Blog archive (100+), Forbes, Entrepreneur, Buffer |
| **Interviews/Podcasts** | @youtube-specialist | All 10 podcast interviews + Perpetual Traffic archive |
| **Video** | @youtube-specialist | Smart Marketer YouTube channel (50+) |
| **Courses** | @web-specialist | Smart Marketer platform (course outlines + testimonials) |
| **Social** | @social-specialist | Social media posts (if collected) |

---

## PARALLELIZATION STRATEGY

**Execute in 3 batches (can run in parallel):**

### Batch 1: CRITICAL (Execute Immediately)
- Duration: 4-6 hours
- Concurrency: Max 3 parallel downloads
- Sources: 8 (Click Happy, blog archive, 4 interviews, Perpetual Traffic)
- **Success target: 100%**
- **Blocking:** Must complete before Batch 2

### Batch 2: IMPORTANT (Run in Parallel with Batch 1)
- Duration: 3-4 hours
- Concurrency: Max 5 parallel downloads
- Sources: 8 (4 interviews, courses, YouTube, case studies)
- Success target: >90%
- **Can run simultaneously with Batch 1**

### Batch 3: NICE-TO-HAVE (Optional)
- Duration: 1-2 hours
- Concurrency: Max 10 parallel
- Sources: 6 (secondary sources, social media)
- Success target: >80%
- **Skip if time-constrained**

---

## OUTPUT STRUCTURE EXPECTED

```
squads/mmos-squad/minds/molly_pittman/sources/
├── sources_master.yaml              (ONLY metadata file in /sources)
├── blogs/
│   ├── how-to-be-successful.md
│   ├── 5-key-elements-facebook-ad.md
│   └── [100+ blog posts as markdown]
├── youtube/
│   ├── marketing-2025-parker-nash/
│   │   ├── transcript.md
│   │   └── metadata.json
│   ├── perpetual-traffic-ep-001/
│   │   ├── transcript.md
│   │   └── metadata.json
│   └── [podcast archives with transcripts]
├── pdf/
│   ├── click-happy-book/
│   │   ├── text.md
│   │   └── metadata.json
│   └── coauthored-book/
│       ├── text.md
│       └── metadata.json
└── manual/
    └── [templates for manual collection if needed]

docs/logs/
├── 2026-02-15T00-00-00Z-collection-report.yaml
├── 2026-02-15T00-00-00Z-temporal-context.yaml
└── [other collection logs]
```

**CRITICAL:** All reports/logs go to `docs/logs/`, NOT `sources/`

---

## COLLECTION PARAMETERS

### API Keys / Authentication
Ensure these environment variables are set:
- `ASSEMBLYAI_API_KEY` — For podcast transcription
- YouTube API key (if using official API)
- Any other platform credentials needed

### Download Rules
- Respect robots.txt
- Use appropriate User-Agent
- Implement rate limiting
- Max 10 concurrent downloads total
- Exponential backoff: initial 1s, max 30s, multiplier 2x

### Quality Standards
- **Tier 1 success rate:** 100% (blocking)
- **Tier 2 success rate:** ≥90% (warning if <80%)
- **Tier 3 success rate:** ≥80%
- **Metadata completeness:** 100% for all downloads
- **File integrity:** Validate checksums

### Error Handling
- Max 3 retries per source
- Log all failures with timestamps
- Generate detailed error report
- Flag permanent failures vs. temporary

---

## VALIDATION CHECKLIST

Before declaring collection complete, validate:

- [ ] All 8 Tier 1 sources collected (100%)
- [ ] At least 7/8 Tier 2 sources collected (>90%)
- [ ] Metadata extracted for each source
- [ ] No corrupted files
- [ ] Podcast transcripts generated (AssemblyAI or captions)
- [ ] Blog posts converted to markdown with frontmatter
- [ ] Book PDFs extracted to text
- [ ] Directory structure matches output specification
- [ ] Collection report generated (COLLECTION_SUMMARY.yaml)
- [ ] All files organized with semantic slugs (not T1-001)

---

## SUCCESS CRITERIA

**Collection is successful when:**

1. ✅ All 8 Tier 1 sources collected (Click Happy, blog, 4 interviews, Perpetual Traffic)
2. ✅ Metadata preserved for all sources
3. ✅ Transcripts extracted for all audio/video
4. ✅ Files organized in correct directories
5. ✅ sources_master.yaml ready for Phase 2
6. ✅ No blocking errors reported
7. ✅ Tier 2 sources mostly collected (>90%)

**If successful:**
- Proceed to Phase 2: Cognitive Analysis (8-layer extraction)
- Activate: @daniel-behavioral-analyst, @barbara-cognitive-architect, @cognitive-analyst, @identity-analyst

---

## HANDOFF INSTRUCTIONS

**@data-collector: Execute the following:**

1. Load batch configuration files (tier1_batch.yaml, tier2_batch.yaml, tier3_batch.yaml)
2. Route sources to appropriate specialist agents
3. Execute Batch 1 & 2 in parallel (max 3 + max 5 concurrent)
4. Monitor progress and report blockers
5. Validate completeness using checklists
6. Generate COLLECTION_SUMMARY.yaml
7. Report final status to Mind Mapper

**Command:** Execute full parallel collection from batch YAML files

**Expected Duration:** 2-4 hours total

---

## CONTACT / STATUS UPDATES

- Report progress every 30 minutes during collection
- Flag any Tier 1 failures immediately
- Final report when complete
- Ready for handoff back to Mind Mapper for Phase 2 (Analysis)

---

**Status:** ✅ Ready for ETL Execution
**Priority:** High (critical for MMOS pipeline)
**Date Prepared:** 2026-02-15
**Prepared By:** Mind Mapper (MMOS Orchestrator)
