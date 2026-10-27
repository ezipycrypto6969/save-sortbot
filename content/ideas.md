# Content backlog

Breakdowns from the founder's own saved reels. Each one can become a reel (breakdown or scam-watch format).
Mark an idea `[used YYYY-MM-DD]` after it's been queued. Never name or tag the original creator; paraphrase their claim in a few words.

## 000 · AI & tools · breakdown
**Claim in the reel:** Harvey: a free, open-source Claude Code agent that finds leads (via OpenStreetMap), scores them, drafts personalised cold emails and runs your sales pipeline. Every email waits for your approval.
**What it really is:** A free, open-source sales agent that runs on your own computer using Claude Code. It finds local businesses, checks their websites, scores each one against your ideal customer, writes a personalised cold email about something specific it found, then tracks replies and pushes each conversation toward a meeting.
**Tools:** Harvey on GitHub (https://github.com/ethanplusai/harvey); Setup walkthrough (https://www.kevinsingh.com/p/harvey-set-up-the-open-source-claude); Claude Pro or Max (https://claude.com/pricing); Google Workspace (https://workspace.google.com)
**Steps:** Decide exactly what you sell and to whom, e.g. '5-page websites for Perth physios'. Harvey is only as good as this sentence. | Buy a second domain (not your main one), set up a Google Workspace mailbox on it, and turn on SPF, DKIM and DMARC. Warm it up for 2–4 weeks before real sending, otherwise you land in spam. | Install Python 3.11+ and Claude Code, run `claude login`, then clone the repo. Easiest path: open Claude Code in the folder and say 'set Harvey up for me'. | Run `harvey train https://your-site.com`, then `harvey discover` to find businesses, `harvey dashboard` for the pipeline view, and `harvey run` to start the loop. | Read and approve every email in the Outbox (approval is on by default). Start at 10–20 a day and keep bounces under ~3%.
**Benefit:** This is the client-finding engine for any service you sell (websites, AI receptionists, Google profile setup). It replaces hours of searching, researching and writing cold emails each week.
**Cost:** Software free. Claude Pro (US$20/mo) or Max. Domain ~A$15/yr. Workspace ~US$7/mo. Lead data: OpenStreetMap is free, DataForSEO about US$0.37 per 1,000 businesses.
**Catch:** In Australia cold email falls under the Spam Act 2003: only email published business addresses about things relevant to that business, name yourself, and include an unsubscribe. OpenStreetMap data is thin for tradies (plumbers, roofers). Your computer has to stay on while it runs.

## 002 · AI & tools · breakdown
**Claim in the reel:** Stiles AI had an AI go through 70 saved reels and turn the useful ones into reusable Claude skills. This is the idea behind this page.
**What it really is:** The creator had an AI go through 70 saved reels and turn the useful, repeatable ones into Claude 'skills': saved instructions Claude follows every time you ask for that task.
**Tools:** Claude skills (https://support.claude.com)
**Steps:** Export your saves (done: that's this page). | Pick the reels that describe a repeatable process, not motivation. From your saves: Harvey setup, AI receptionist pitch, Google Business Profile audit, Meta Ad Library research. | Ask Claude: 'turn this into a skill' and paste the breakdown from this page. | Save it, then reuse it by name any time, e.g. 'run my GBP audit on Joe's Plumbing'.
**Benefit:** You stop re-explaining the same task. Each skill becomes a mini-product you can run for clients in minutes.
**Cost:** Included in your Claude plan.
**Catch:** Most reels are hype, not processes. Only about 1 in 7 of your saves is worth turning into a skill.

## 003 · AI & tools · breakdown
**Claim in the reel:** Give Claude Code its own phone number (via a Bland API key) so it calls you when it needs a decision, then keeps working.
**What it really is:** Connects Claude Code to Bland, an AI phone-call service, so a long-running coding task rings you when it needs a decision. You answer by voice, and the transcript goes back into the session.
**Tools:** Bland AI (https://www.bland.ai); Claude Code (https://claude.com/claude-code)
**Steps:** Create a Bland account and copy your API key. | Ask Claude Code to write a small tool that calls the Bland API to phone you with a question and waits for the transcript. | Tell Claude Code to use that tool whenever it's blocked on a decision. | Test with a small task before trusting it on anything big.
**Benefit:** Lets long builds keep moving while you're away from the desk.
**Cost:** Bland's free Start plan, then about US$0.09 per connected minute.
**Catch:** The full guide is gated behind 'comment PHONE'. For most people it's simpler to check running tasks from the Claude phone app.

## 004 · AI & tools · breakdown [used 2026-10-27]
**Claim in the reel:** Dan Martell on how to get useful answers from AI models. The caption gives no detail.
**What it really is:** The caption only says 'how to get useful answers from AI models'. Here's the general technique.
**Steps:** Give context: who you are, what it's for, who will read it. | Show an example of what good looks like. | Ask it to ask you questions before answering. | Ask for options, then pick and refine.
**Benefit:** Better output on every task.

## 006 · AI & tools · breakdown
**Claim in the reel:** 3 Claude skills for better-looking websites: Emil Kowalski's design skills (animation), Impeccable (layout, type, colour), Taste (unique designs, real photos), plus Figma MCP.
**What it really is:** Three add-on skills that make websites built by Claude look professionally designed instead of generic.
**Tools:** Impeccable (Paul Bakaus) (https://www.claudepluginhub.com/plugins/pbakaus-impeccable); Taste (Lead Gen Jay) (https://leadgenjay.com/skills/taste); Emil Kowalski's design skill (https://github.com/emilkowalski/skill); Playwright (https://playwright.dev); Figma MCP (https://www.figma.com)
**Steps:** Install Claude Code (also in the desktop app's Code tab). | Add the skills: copy each skill folder into your Claude skills folder, or install as a plugin where offered. | Build the site, then ask: 'run Impeccable /audit, fix everything, then /polish'. | Ask Claude to test it with Playwright at phone and desktop width before you show the client.
**Benefit:** If you sell websites, better-looking output means you can charge more and need fewer revisions.
**Cost:** The skills are free. You need a Claude plan.
**Catch:** The 'comment DESIGN' setup is a lead magnet; everything you need is linked here. You still need your own eye: always check it on a phone.

## 007 · AI & tools · breakdown
**Claim in the reel:** Vision of an AI 'operating system' that reads your email, organises files and flags what needs attention.
**What it really is:** An 'AI operating system' that reads your email, organises files and tells you what needs attention. Claude can already do most of this today.
**Tools:** Claude connectors (https://claude.com)
**Steps:** In Claude settings, connect Gmail, Calendar and Drive. | Ask: 'what in my inbox needs a reply today?' | Set a scheduled task for a weekday morning brief.
**Benefit:** Saves time daily. Setting this up for busy business owners is also a sellable service.
**Cost:** Claude plan.
**Catch:** Only connect accounts you're comfortable letting Claude read.

## 009 · AI & tools · breakdown
**Claim in the reel:** After 3,000 hours in Claude: skip the chat, drive Claude Code from the terminal so it runs jobs start to finish.
**What it really is:** Instead of chatting and copy-pasting, you give Claude Code a job and it runs commands, edits files and finishes it end to end.
**Tools:** Claude Code (https://claude.com/claude-code); Docs (https://docs.claude.com/en/docs/claude-code/overview)
**Steps:** Open the Code tab in the Claude desktop app (no terminal needed), or install the CLI. | Point it at a folder and give it a whole job: 'build a 5-page website for a Perth physio, test it, and tell me how to publish it'. | Review what it changed before you ship anything to a client.
**Benefit:** This is how one person delivers websites, tools and automations fast enough to make a service business work.
**Cost:** Included with Claude Pro and above.
**Catch:** Learning curve of a few days. Always review its work.

## 010 · Marketing & ads · breakdown
**Claim in the reel:** Trend-jacking (riding current trends) as a content growth tactic.
**What it really is:** Trend-jacking means riding a trend that's already popular (a sound, format or news story) to get your content seen. The caption has no detail.
**Steps:** Check trending audio in Instagram's Reels tab daily. | Make your version within 24–72 hours, tied to your niche. | Post fast. Trends die in days.
**Benefit:** Cheap reach for a new account.

## 011 · Marketing & ads · breakdown
**Claim in the reel:** An AI content system that replaced a marketing team. 'Comment for access' lead magnet.
**What it really is:** An AI content system for marketing. The 'free system' is a comment-gated lead magnet. Here's the general idea.
**Steps:** Use Claude to turn one idea into scripts, captions and carousel text. | Batch-film once a week. | Repurpose each video across Instagram, TikTok and YouTube Shorts.
**Benefit:** Consistent posting without a team.

## 013 · Tech & privacy · breakdown
**Claim in the reel:** How your SIM's ICCID and IMSI act as a fingerprint that forensic tools can trace to a subscriber.
**What it really is:** Your SIM has two IDs (ICCID for the card, IMSI for your subscription), your phone has an IMEI, and carriers log which towers you connect to. With legal process, investigators can link them all together.
**Benefit:** Good to know for privacy: changing your SIM doesn't make you anonymous.

## 015 · Money & finance · breakdown
**Claim in the reel:** Parable of four brothers with $100 each: one used leverage and made 561x more.
**What it really is:** A parable: four brothers each get $100 and one makes 561x more through leverage, by making money work without trading more of his own hours.
**Steps:** The four kinds of leverage: other people's time (hiring), money (capital), code (software and AI) and media (content). | Code and media need no one's permission. That's why AI and content side hustles scale.
**Benefit:** Aim for work where income isn't capped by your hours.

## 016 · Money & finance · breakdown
**Claim in the reel:** 1,149 of 4,299 Australian companies earning $100M+ paid no income tax in 2024–25 (ATO), using legal profit-shifting.
**What it really is:** ATO data: 1,149 of the 4,299 companies earning $100M+ paid no income tax in 2024–25. Often legal (losses, offsets, profit shifting), though the ATO says paying no tax doesn't necessarily mean wrongdoing.
**Tools:** ATO Corporate Tax Transparency (https://www.ato.gov.au/about-ato/research-and-statistics/in-detail/corporate-tax-transparency)
**Benefit:** News. For your own side hustle: get an ABN, track expenses, and claim legitimate deductions.

## 017 · AI & tools · breakdown [used 2026-10-27]
**Claim in the reel:** Six prompts that turn Claude into a tutor who pushes back instead of handing you answers.
**What it really is:** Prompts that make Claude teach like a tutor: asking you questions and making you work it out, instead of handing over answers. The six prompts are in the video, not the caption.
**Steps:** Start with: 'Be my tutor for [skill]. Don't give me answers. Ask me one question at a time, push back when I'm wrong, and only explain after I've tried.' | Add: 'Quiz me at the end and tell me my weakest area.' | Use it on skills you'll sell, like copywriting, Meta ads or basic coding.
**Benefit:** You learn faster and actually retain it, which matters more than any tool.
**Cost:** Free with any Claude plan.

## 018 · AI & tools · breakdown
**Claim in the reel:** An email automation trick (Composio partner). The caption gives no detail.
**What it really is:** The tag points to Composio, a tool that connects AI agents to apps like Gmail. The specific trick is only in the video.
**Tools:** Composio (https://composio.dev)
**Steps:** Inside Claude you can skip Composio: connect the Gmail connector and ask Claude to triage or draft replies.
**Benefit:** Faster inbox handling.

## 019 · Business & side hustles · breakdown
**Claim in the reel:** Goal + deadline + plan + consistency: build systems, not just goals. Lead-gen pitch.
**What it really is:** Goal + deadline + plan + consistency. Build systems, not just goals.
**Steps:** Set a 90-day goal (e.g. 3 paying clients). | Turn it into weekly actions (e.g. 50 outreach emails). | Track it weekly.

## 020 · Ecommerce · breakdown
**Claim in the reel:** Breakdown of scaling branded dropshipping from zero to $1,000/day (DM for doc).
**What it really is:** Branded dropshipping: you sell under your own brand while a supplier ships the products. The full guide is a DM lead magnet.
**Steps:** Pick one product with a clear problem/solution and good margins. | Build a branded store (Shopify or similar). | Make your own content and ads (see Meta Ad Library + Starpop). | Move to faster or local suppliers once something sells.
**Cost:** Store ~US$30–40/mo plus ad testing budget (often A$500+).
**Catch:** '$1,000/day' is the best case. Most stores fail on ad costs. Australian Consumer Law guarantees still apply to you as the seller: refunds, and accurate shipping times.

## 023 · Ecommerce · scam-watch [used 2026-10-27]
**Claim in the reel:** Claim that 'GPT Astra' clones any ecom store in minutes (Amboras promo).
**What it really is:** Promo for Amboras, a Y Combinator-backed AI store builder: you describe what you sell and it builds the store, writes copy and connects checkout.
**Tools:** Amboras (https://www.amboras.com)
**Steps:** Try it free to compare it with Shopify for a test store.
**Catch:** These are sponsored posts. 'Clone any store' is a bad idea: copying another brand's design, photos or text breaches copyright and trademark.

## 027 · Tech & privacy · scam-watch
**Claim in the reel:** Rundown of controversial surveillance/AI tools, including Heretic, which strips refusals from AI models.
**What it really is:** Three open-source projects: Heretic (strips the safety refusals out of open AI models), God's Eye View (a 3D globe of public flight, ship, satellite and CCTV data) and Meta's Brain2Qwerty (reconstructs typed sentences from brain scans in a lab).
**Tools:** God's Eye View (https://github.com/bilawalsidhu/gods-eye-view); Brain2Qwerty (https://github.com/facebookresearch/brain2qwerty)
**Benefit:** Interesting news. Nothing here is a money-maker.
**Catch:** Models with their safety training removed will help with harmful things and are a live ethics debate. Not something to build a business on.

## 028 · Business & side hustles · breakdown [used 2026-10-27]
**Claim in the reel:** Businesses that get people off their phones and present will become very valuable.
**What it really is:** Businesses that give people a reason to put their phones down (in-person, social, present) are becoming more valuable.
**Steps:** Ideas: phone-free run club, board-game or trivia nights, hands-on workshops (pottery, cooking, woodwork), phone-free events at cafés. | Start small: one event, a Facebook/Instagram page, charge per ticket.
**Benefit:** Low startup cost and a strong trend behind it.

## 029 · Marketing & ads · breakdown
**Claim in the reel:** Meta ads tips for agencies. The caption gives no detail.
**What it really is:** Meta ads tips for agencies. The detail is only in the video.
**Steps:** See the Meta Ad Library breakdown for the free research method.

## 031 · AI & tools · breakdown
**Claim in the reel:** A Claude skill that spins up many subagents and picks the best output ('Comment arena').
**What it really is:** Have Claude run several independent attempts at the same task in parallel (subagents) and pick the best one.
**Tools:** Claude Code subagents (https://docs.claude.com/en/docs/claude-code/overview)
**Steps:** In Claude Code, ask: 'spawn 3 subagents to each write the homepage copy independently, then compare them and combine the best parts'. | Use it for work where quality matters: sales pages, ad scripts, pitch emails.
**Benefit:** Better first drafts and less re-prompting.
**Cost:** Uses your usage limit several times faster.
**Catch:** '100 subagents' is hype. 3–5 is the practical number.

## 036 · Ecommerce · breakdown
**Claim in the reel:** Claims Claude Opus 5.5 'changed ecom forever' (Amboras promo).
**What it really is:** Another Amboras promo, this time pairing it with Claude Opus 5.5.
**Steps:** See the Amboras breakdown.

## 040 · Tech & privacy · breakdown
**Claim in the reel:** WatchTower app maps 580,000+ public surveillance cameras, works offline.
**What it really is:** An app said to map 580,000+ documented public cameras (CCTV, licence-plate readers, speed and red-light cameras), viewable offline.
**Catch:** I couldn't verify this app. Similar projects (like DeFlock) mainly cover the US. Treat it as news, not a tool.

## 043 · Business & side hustles · scam-watch [used 2026-10-27]
**Claim in the reel:** Real-estate wholesaling/assignment scheme the creator admits is a legal grey area that can cost you a licence.
**What it really is:** A scheme to approach home sellers, help them avoid agent fees and take a cut. The creator admits it's a legal 'grey area'.
**Tools:** WA Consumer Protection: real estate licensing (https://commerce.wa.gov.au/consumer-protection/licensing-and-registration-real-estate)
**Steps:** Don't do this in Australia. In WA anyone acting as a real estate agent must be licensed under the Real Estate and Business Agents Act 1978, and taking a fee to help sell someone's house without a licence breaks it. | Legit route: get a sales representative registration through a real estate course, or offer services that don't involve selling, like listing photos, video tours or copywriting for private sellers.
**Catch:** Fines and a ban from the industry. Not worth it.

## 045 · Business & side hustles · breakdown
**Claim in the reel:** Localize, an app to find local farms, pitched against corporate food consolidation.
**What it really is:** Localize is a US app (50,000+ farmers) that lets you buy directly from local farms.
**Benefit:** Business angle for you: a Perth version (directory or newsletter of local farms, markets and producers) or doing social media and websites for local farms.
**Catch:** The app itself is US-focused.

## 047 · Marketing & ads · breakdown [used 2026-10-27]
**Claim in the reel:** You need marketing, proof (testimonials) and branding together to grow a brand.
**What it really is:** Growing a brand needs three things together: marketing (people know you exist), proof (people believe you) and branding (you stand out).
**Steps:** Collect a testimonial or Google review after every job. | Post before-and-after or results content weekly. | Keep one consistent look and name everywhere.
**Benefit:** Proof is what turns views into paying customers.

## 050 · Business & side hustles · breakdown
**Claim in the reel:** Day 6 of growing a pressure-washing business to $5,000.
**What it really is:** Someone documenting growing a pressure-washing business day by day.
**Steps:** See the 'home services' breakdown (adamrchap). Same playbook.
**Benefit:** Documenting your own journey on Instagram is free marketing.

## 051 · AI & tools · breakdown [used 2026-10-27]
**Claim in the reel:** Dan Martell on stopping AI from being a yes-man.
**What it really is:** Making AI disagree with you instead of agreeing with everything. The caption has no detail; here's the technique.
**Steps:** 'Argue against my plan as hard as you can.' | 'Rate this 1–10 and list what would make it a 10.' | 'What would a sceptical customer say?'
**Benefit:** Catches bad ideas and weak work before a client does.

## 053 · Marketing & ads · breakdown [used 2026-10-27]
**Claim in the reel:** Making AI animated ads with Starpop.ai, plus a Claude skills swipe file.
**What it really is:** Starpop is an AI tool for making paid social ads (scripts, AI video and images) for Meta, TikTok and YouTube.
**Tools:** Starpop (https://starpop.ai)
**Steps:** Research winning competitor ads first (Meta Ad Library). | Generate several script variations in Starpop or Claude. | Produce 3–5 versions and test them with a small budget. | Keep the winner and kill the rest.
**Benefit:** Lets one person produce ad creative fast. You could sell ad creative to small ecommerce brands.
**Cost:** Usage-based credits. Price isn't published, so check the site.
**Catch:** Don't present AI actors as real customers giving testimonials. That's misleading advertising under Australian Consumer Law (ACCC).

## 054 · Marketing & ads · breakdown
**Claim in the reel:** Tool to spy on competitor brands' top-performing Meta ads.
**What it really is:** The reel pushes a paid tool to 'spy' on competitors' winning ads. You can do this for free with Meta's own Ad Library.
**Tools:** Meta Ad Library (https://www.facebook.com/ads/library); AdManage.ai (https://admanage.ai)
**Steps:** Open the Ad Library, set country to Australia, search a competitor or keyword. | Look for ads that have been running for weeks or months. Brands keep paying for ads that work. | Note the hook (first 3 seconds), the offer and the format. | Paste the best ones into Claude and ask for 5 original variations for your product.
**Benefit:** Free market research before you spend a cent on ads.
**Cost:** Free.
**Catch:** Copy the idea, not the ad. Copying wording or visuals can breach copyright.

## 055 · Business & side hustles · breakdown
**Claim in the reel:** Positioning yourself in the health & wellness market in 2026.
**What it really is:** A pitch about positioning in health & wellness. The breakdown is gated behind a comment.
**Benefit:** Health & wellness brands spend heavily on content and ads, so they're a good niche for marketing services.

## 059 · Business & side hustles · breakdown
**Claim in the reel:** Home services (gutters, window washing) are a simpler path than an AI startup; homeowners happily pay $300.
**What it really is:** Skip the AI startup. Homeowners will happily pay $250–300 to avoid cleaning gutters or washing high windows, and one job can lead to a whole street.
**Tools:** ABN registration (https://www.abr.gov.au); Google Business Profile (https://business.google.com)
**Steps:** Pick one service: gutter cleaning, window washing, pressure washing or Christmas light installs. | Get an ABN (free) and public liability insurance. | Set up a Google Business Profile (see the GBP breakdown) and a simple website. | On every job, drop 20–30 door hangers on the street, put a yard sign out the front, and ask for a Google review. | Upsell by season: gutters → windows → driveway → Christmas lights. | Once you're booked out, hire, and move to marketing and scheduling yourself.
**Benefit:** Fast cash, low startup cost, repeat customers. Combine it with an AI receptionist and Harvey for leads.
**Cost:** Gear from a few hundred dollars (ladder, brushes) to ~A$1,500 for a decent pressure washer and surface cleaner, plus insurance.
**Catch:** Physical work. Working at heights is dangerous, so follow WorkSafe WA guidance. Check council rules on runoff into storm drains.

## 060 · AI & tools · breakdown
**Claim in the reel:** Most of the world still hadn't used generative AI in late 2025, so it's still early.
**What it really is:** Most people worldwide still hadn't used generative AI as of late 2025.
**Steps:** Target small local businesses, not tech people. | Sell outcomes (more bookings, fewer missed calls), not 'AI'.
**Benefit:** Your real market is the plumber, café owner or physio who has never touched AI. They'll pay for someone to set it up for them.

## 062 · Tech & privacy · scam-watch [used 2026-10-27]
**Claim in the reel:** Offline survival AI device prototype (preorder promo).
**What it really is:** An 'offline survival AI' gadget on preorder.
**Steps:** Before preordering, look at Project N.O.M.A.D. (next breakdown): a free, open-source version of the same idea.
**Catch:** Preorder hype with no specs in the caption.

## 064 · Marketing & ads · breakdown
**Claim in the reel:** Marketing to one person to make them believe a product was viral.
**What it really is:** A story about targeting ads so narrowly at one person that he thought the product was everywhere.
**Benefit:** Lesson: tight targeting (one company, one suburb, one job title) is cheap and powerful for B2B and local services.

## 067 · Marketing & ads · breakdown
**Claim in the reel:** Meta ads help offer.
**What it really is:** A 'comment SCALE' pitch for Meta ads help. There's no actual tip in the caption.
**Steps:** See the Meta Ad Library breakdown.

## 071 · Money & finance · breakdown
**Claim in the reel:** Story of an insurance death-benefit finder who kept a large cut.
**What it really is:** A story about someone who tracks down families owed insurance payouts and takes a big cut.
**Tools:** ASIC unclaimed money search (https://moneysmart.gov.au/find-unclaimed-money); Lost super (via myGov/ATO) (https://www.ato.gov.au/individuals-and-families/super-for-individuals-and-families/super/check-your-super-balance-and-find-lost-super)
**Steps:** Search your name and your family's names on Moneysmart for free. | Check for lost super through myGov.
**Benefit:** In Australia you don't need a middle-man: the search is free.

## 072 · Marketing & ads · breakdown [used 2026-10-27]
**Claim in the reel:** Make your offer obvious, simple and low-friction.
**What it really is:** Make your offer obvious, simple and low-friction.
**Steps:** Write your offer in one sentence: 'I'll [result] for [who] in [time] for [price].' | Add a guarantee that removes the risk. | Give one clear next step (book a call, reply YES). | Cut everything else.
**Benefit:** Simple offers convert better, especially in cold emails and DMs.
**Cost:** Free.

## 077 · Business & side hustles · breakdown
**Claim in the reel:** A Melbourne logistics business expects AI to double its workforce in 12 months.
**What it really is:** A Melbourne logistics business expects AI to double its workforce in 12 months: AI is creating jobs there, not cutting them.
**Benefit:** Businesses are hiring people who can set up and run AI tools. That's the skill set behind this page.

## 082 · Business & side hustles · breakdown
**Claim in the reel:** Detailing shops fall apart without written systems: inspection sheets and standard procedures.
**What it really is:** Service businesses fall apart when the standard is only in the owner's head. The fix is written systems: an inspection sheet, a step-by-step checklist and a final quality check on every job.
**Steps:** Write down every step of your service in order. | Turn it into a one-page checklist (Claude can format it). | Add a before-photo and inspection step and a final QC step. | Make every job follow it, no matter who does it.
**Benefit:** Lets you hire without quality dropping. 'I'll write your SOPs and checklists' is also a sellable service to tradies and detailers.
**Cost:** Free.

## 084 · Money & finance · breakdown
**Claim in the reel:** Jamie Dimon stayed calm through 2008 by switching JPMorgan into crisis mode.
**What it really is:** Jamie Dimon kept JPMorgan steady in 2008 by moving fast: daily risk meetings, the right people, quick decisions.
**Benefit:** Lesson: in a crisis, act on information instead of worrying.

## 085 · AI & tools · breakdown
**Claim in the reel:** Building a self-correcting multi-agent system in Python with Google's Agent Development Kit (ReAct, agent patterns).
**What it really is:** A tutorial building a self-correcting multi-agent blog writer in Python with Google's Agent Development Kit: a planner agent, a writer agent, and a checker that loops until the output passes.
**Tools:** Google ADK docs (https://google.github.io/adk-docs/); Gemini API key (https://aistudio.google.com)
**Steps:** Install Python and uv, then follow the ADK quickstart. | Build the three parts: planner → writer → validator in a loop. | Test in the ADK web UI. | Or describe the same design to Claude Code and have it build it for you.
**Benefit:** Agent-building is a sellable skill: content pipelines, research bots, lead qualifiers.
**Cost:** Free to learn; model usage is cheap at small scale.
**Catch:** Needs basic Python. Start with Claude Code if you don't code.

## 090 · AI & tools · breakdown
**Claim in the reel:** 7 prompts for ADHD task paralysis (e.g., break a task into sub-1-minute steps). The 'feature' framing is hype; the prompts are usable.
**What it really is:** Prompts for task paralysis and focus. The 'ADHD Executive Function Mode' isn't a real Claude feature. These are just prompts, but they're good ones.
**Steps:** Task Paralysis Shatterer: 'I am staring at [task] and can't start. Break it into steps under 1 minute each. Give me only the first step.' | Dopamine Menu: 'Make me a menu of 5-min movement breaks, 20-min deep-work blocks and 10-min creative breaks.' | Body Double: 'Act as my body double for 30 minutes and check in every 10 minutes for a status update.' | Context Switch: 'I finished [A] and need to start [B]. Give me a 3-minute reset routine.' | Gamify: 'Turn this boring task into a quest linked to my interest in [X], with a reward at the end.' | Time-Blindness Audit: 'I think [project] takes 20 minutes but it takes 2 hours. Help me estimate realistically.'
**Benefit:** Gets you started on the boring parts of a side hustle (admin, outreach, invoices).
**Cost:** Free.

## 091 · AI & tools · scam-watch
**Claim in the reel:** 'Founder Thinking Mode' prompts for business ideas. Not a real Claude feature, just prompting.
**What it really is:** 'Founder Thinking Mode' is not a real Claude feature. The idea of using Claude as a business sparring partner is good, though.
**Steps:** Prompt: 'Pressure-test this business idea like a sceptical investor. Who pays, how much, how do I reach them, what's the cheapest test I can run this week, and what kills it?' | Then: 'Give me a 7-day plan to get my first paying customer.'
**Benefit:** Kills bad ideas before you spend money on them.
**Cost:** Free.
**Catch:** Posts that invent 'secret modes' are engagement bait. Be sceptical of that creator's other claims.

## 094 · Business & side hustles · breakdown
**Claim in the reel:** Being smart isn't a business model; execution beats IQ.
**What it really is:** Being smart isn't a business model. Execution beats IQ.
**Benefit:** Pick one breakdown on this page and do it this week.

## 097 · Tech & privacy · breakdown [used 2026-10-27]
**Claim in the reel:** Open-source offline computer project that keeps working when the internet is down.
**What it really is:** Project N.O.M.A.D., a free open-source offline 'survival computer': offline Wikipedia, a local AI assistant, offline maps and Khan Academy courses, all working with no internet.
**Tools:** Project N.O.M.A.D. on GitHub (https://github.com/Crosstalk-Solutions/project-nomad); Hardware guide (https://projectnomad.us/hardware)
**Steps:** Use an old PC or a mini PC with plenty of storage. | Install Docker, then follow the repo's install guide. | Download the content packs you want (Wikipedia is 11–100 GB).
**Benefit:** A fun build and a portfolio piece. You could also sell pre-built units to preppers or remote properties.
**Cost:** Software free. Storage and hardware are the cost.

## 120 · Money & finance · breakdown
**Claim in the reel:** Bill Ackman's comeback after losing $4B on Valeant.
**What it really is:** Bill Ackman lost $4B on Valeant and rebuilt to a $9.3B net worth through discipline.
**Benefit:** Lesson: one big loss isn't the end. Don't bet everything on one position.

## 123 · Marketing & ads · breakdown
**Claim in the reel:** Real-estate agent's viral house video (7M views).
**What it really is:** A real estate agent got 7M views on a fun, personality-driven listing video.
**Benefit:** Lesson for any local business: personality plus a hook beats polished-but-boring. Making these videos for agents is a sellable service.

## 124 · Marketing & ads · breakdown
**Claim in the reel:** Tip to rank your Google Business Profile higher (tradies/services).
**What it really is:** How to make a business rank higher on Google Maps. This is where tradies and local services get most of their calls.
**Tools:** Google Business Profile (https://business.google.com)
**Steps:** Claim and verify the profile. | Choose the most specific primary category (e.g. 'Gutter cleaning service', not 'Contractor') and add secondary ones. | Fill in everything: service areas, hours, a services list with descriptions, phone, website. | Upload real photos every week (jobs, team, van). | Get reviews: ask every customer with a direct link, and reply to every review. | Post updates and offers regularly, and keep name, address and phone identical everywhere online.
**Benefit:** More calls for free. Side hustle: charge local businesses to set up and optimise their profile. Claude can audit a profile and write the content.
**Cost:** Free.
**Catch:** Never buy or fake reviews. Google removes them and the ACCC treats fake reviews as misleading conduct.

## 127 · Tech & privacy · breakdown [used 2026-10-27]
**Claim in the reel:** Using Claude to clean your data off the internet: data-broker opt-outs, account deletions, CCPA/GDPR requests.
**What it really is:** Using Claude to remove your personal data from the internet: data-broker listings, old accounts and breached logins.
**Tools:** Have I Been Pwned (https://haveibeenpwned.com); JustDeleteMe (https://justdeleteme.xyz); Google 'Results about you' (https://support.google.com/websearch/answer/12719076)
**Steps:** Run your emails through Have I Been Pwned and change passwords (use a password manager) on anything breached. | List every old account you remember. Ask Claude to look up deletion steps (via JustDeleteMe) and draft the requests. | Google your name, phone and address, and use 'Results about you' for removals. | Ask Claude to draft deletion and correction requests to any site holding your data.
**Benefit:** Less spam, less scam risk, less identity theft risk.
**Cost:** Free.
**Catch:** The US/EU laws in the reel (CCPA, GDPR) mostly don't apply to Australians. Australian sites fall under the Privacy Act 1988, which gives you rights to access and correct your data. Full deletion isn't always guaranteed.

## 136 · AI & tools · breakdown
**Claim in the reel:** Alexandr Wang's 100-person AI lab at Meta and his advice to kids.
**What it really is:** Alexandr Wang (Scale AI founder, now leading an AI lab at Meta) says AI will write most code within five years and young people should learn to build with AI coding tools.
**Steps:** Pick one small real project: a site for a family member's business, or a calculator for a trade. | Build it with Claude Code this week.
**Benefit:** Building things with AI is the skill behind nearly every side hustle on this page.

## 137 · Business & side hustles · breakdown
**Claim in the reel:** Brex CEO: there's no shortcut to $1M in 90 days; build real value.
**What it really is:** Brex's CEO says there's no way to make $1M in 90 days. Real wealth takes value and patience.
**Benefit:** A good filter for every 'get rich' reel on this page.

## 139 · AI & tools · breakdown
**Claim in the reel:** Building apps with Lovable.dev (sponsored).
**What it really is:** Lovable builds web apps from a text prompt (this post was sponsored).
**Tools:** Lovable (https://lovable.dev)
**Steps:** Describe the app in plain English. | Iterate on it in the editor. | Publish, or export the code.
**Benefit:** Quick prototypes or simple apps for clients.
**Cost:** Free: 5 credits/day (30/month). Pro: US$25/mo.
**Catch:** Credits run out fast on bigger apps. Claude Code can do similar work on your existing plan.

## 142 · AI & tools · breakdown
**Claim in the reel:** Build an AI voice receptionist as a side hustle (free guide + prompt).
**What it really is:** Build an AI phone receptionist that answers calls 24/7, answers questions and books appointments, then sell it to local businesses for a monthly fee.
**Tools:** Vapi (https://vapi.ai); Retell AI (https://www.retellai.com); Bland AI (https://www.bland.ai); Claude (https://claude.ai)
**Steps:** Pick a niche that misses calls: tradies on the tools, dentists, salons, mechanics. | Collect the business's hours, services, prices, FAQs and booking rules with a questionnaire. | Have Claude write the receptionist's instructions from that, then build the agent in Vapi or Retell and connect a calendar. | Demo it using that business's own details. Hearing their own business answered is what sells it. | Offer a 14–30 day free trial, then charge setup + monthly.
**Benefit:** Recurring monthly income per client. Missed calls are lost jobs for tradies, so it's an easy pitch.
**Cost:** Vapi ~US$0.05/min platform fee, ~US$0.30/min all-in. Agencies quoted (US figures): $500–1,000 setup and $300–1,000 per month.
**Catch:** Test hard: a bad AI on the phone loses the client customers. Tell callers they're speaking to an AI and check call-recording rules. Confirm the platform supports Australian numbers. Plenty of competitors exist, so pick a niche.

## 148 · Tech & privacy · breakdown
**Claim in the reel:** NetworkChuck: using AI to do 6 hours of dark-web research in 30 minutes.
**What it really is:** NetworkChuck shows using AI to compress 6 hours of dark-web threat research into 30 minutes.
**Tools:** Full video (https://youtu.be/_KzObeom88Y)
**Benefit:** The real lesson: AI speeds up any research job. Security research is a career path (see the cybersecurity breakdown).

## 149 · Tech & privacy · breakdown [used 2026-10-27]
**Claim in the reel:** Free satellite-tracking API, good for a coding practice project.
**What it really is:** Free APIs that give live satellite positions. A good beginner coding project.
**Tools:** N2YO API (https://www.n2yo.com/api/); CelesTrak (https://celestrak.org)
**Steps:** Get a free N2YO API key. | Ask Claude Code: 'build a web page showing what satellites are passing over Perth right now, using the N2YO API'. | Publish it and put it in a portfolio.
**Benefit:** A portfolio project that teaches you APIs, the core skill behind most automations you'd sell.
**Cost:** Free.

## 151 · Tech & privacy · breakdown
**Claim in the reel:** Skills cybersecurity students shouldn't ignore.
**What it really is:** Core skills cybersecurity students shouldn't skip: Linux, networking, Python and security fundamentals.
**Tools:** TryHackMe (https://tryhackme.com); Hack The Box (https://www.hackthebox.com); CompTIA Security+ (https://www.comptia.org/certifications/security)
**Steps:** Learn Linux and networking basics first. | Do TryHackMe beginner paths. | Learn Python for scripting. | Get an entry cert (Security+), then specialise.
**Benefit:** Strong job demand in Australia.
**Cost:** TryHackMe has a free tier. Certs cost a few hundred dollars.
**Catch:** Only ever test systems you have written permission to test.

## 153 · Tech & privacy · breakdown
**Claim in the reel:** How long popular cybersecurity skills take to learn.
**What it really is:** How long popular cybersecurity skills take to learn.
**Steps:** See the cybersecurity skills breakdown above.
