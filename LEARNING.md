# Conversation evidence

AI-drafted task summary, not a transcript or grade. It may be public. Use actual
short words or labeled paraphrases; disclose help and leave missing responses
pending. The learner reviews, corrects or removes new excerpts before commit/push.
Accuracy approval is not proof of understanding. Label simulated trials explicitly.

**Available conversation context:** This chat on October 30 and November 3, 2026. APP-001 excerpts below were reviewed for accuracy and publication by the learner.

## APP-001

- Prediction: Learner paraphrase: the light-background character should feel welcoming to beginners. Later, showing different creatures could encourage players to try deck building and advanced strategies.
- Check interpretation: For the phone-width check, the learner said, “The layout would most likely be out of proportion for a phone screen.” AI clarified that the check catches horizontal overflow, not every readability or visual-balance problem.
- Browser observation: The learner noticed generic symbols instead of the games' actual logos and recommended official logos or iconic characters.
- Keep decision: After AI replaced the symbols with official logos, the learner said, “This revised design is very good, and I would keep it because it is easy to follow and navigate.”
- Review: The learner reviewed the APP-001 summary and replied, “This is accurate,” approving publication.
- Help/gaps: The learner chose the beginner TCG topic, selected First Draw from AI naming suggestions because it felt more beginner-oriented, identified XenoSHIN TCG as their username, and supplied their character artwork. AI supplied the Sage archetype label, promise “Find your game. Make your first move.”, layout, code, original First Draw mark and researched game guidance. The learner ran the full checks in their terminal because the agent environment blocked Chromium startup. AI browser review supplemented the learner's own observations. Accounts, roles and advanced strategy features remain unfinished.
- Evidence links / next step: [APP-001 issue #1](https://github.com/pb392/my-app-studio/issues/1), [PR #2](https://github.com/pb392/my-app-studio/pull/2), [SPEC](SPEC.md). Final normal full check passed: Black, Pylint, 98 foundation tests, 2 homepage contracts and 2 actual Chromium journeys. AI verified that the local receipt matched the final source. The learner approved these excerpts for publication. The learner authorized merge; PR #2 merged, issue #1 closed, and both main-branch CI jobs passed on November 3, 2026.

## APP-002

- Prediction: The learner expected a top-corner sign-in area to become an entry to their profile after login. Asked about visiting the private dashboard directly, they said, “They should be sent to the sign in page if they have not signed into their account.”
- Check interpretation: The test saved a login cookie, logged out, then replayed the old cookie and received the expected 401 Unauthorized. The learner initially thought the cookie had not been saved. AI clarified that it had been saved and that the server invalidated the session. Asked whether the copied cookie would still allow access after logout, the learner answered, “No it would not.” This conclusion followed AI clarification.
- Browser observation: Asked to sign up, log in, log out and reopen the dashboard, the learner reported, “It shows a log in screen instead of a create account screen.” AI explained that logout ends the session without deleting the account, so the login page is expected.
- Keep decision: The learner chose to keep the flow: “I would keep this because it shows that you had created an account, and puts you right into a log in screen.” AI clarified that the login screen alone does not prove an account exists; a successful login provides evidence of that.
- Review: The learner reviewed the APP-002 summary and replied, “This is accurate,” approving publication.
- Help/gaps: AI clarified the difference between a visible navigation link and requesting the private page directly. The learner chose the signed-out redirect. AI proposed the label My dashboard, the HTML/JSON account flow and reuse of prepared password/session helpers, and explained password hashes, signed expiring cookies and server-side logout revocation. The post-login access expectation was proposed by AI; it is not a separate learner explanation. The learner reviewed these APP-002 excerpts for accuracy and approved publication.
- Evidence links / next step: [Issue #3](https://github.com/pb392/my-app-studio/issues/3), [SPEC](SPEC.md). The account flow is implemented locally. Fast cumulative checks passed 104 non-browser tests and 14 contracts, with Black/Pylint passing. AI inspected login/signup layouts and the signed-out dashboard redirect. The learner then ran the full explicit APP-002 check: 104 non-browser tests, 14 contracts and 3 Chromium journeys passed, plus Black and Pylint. AI verified the matching receipt and advanced the marker to 2. The normal full rerun after the marker change passed the same 121 checks; AI verified the current source against its receipt. AI inspected the signed-in dashboard at desktop and phone widths using a disposable local account and confirmed logout returned to login. The learner interpretation, observation and keep decision are recorded above. Summary publication was approved; GitHub completion remains pending.

## APP-003

- Prediction: Pending.
- Check interpretation: Pending.
- Browser observation: Pending.
- Keep decision: Pending.
- Review: Pending.
- Help/gaps: Pending.
- Evidence links / next step: Keep APP-002 before agreeing this lesson.
