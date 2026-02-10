<!-- use these prompts for changes to configuration branhces, skip them for main branch changes -->
**1. Summary**:

What has changed?

Why was this done?

**2. Issues Addressed:**
<!-- Add links to github issue(s) this is related to -->
-

**3. Dependencies (e.g. on payu, model or om3-scripts)**

This change requires changes to (note required version where true):
- [ ] payu:
- [ ] access-om3:
- [ ] om3-scripts:
<!-- Describe and link to the related changes to dependencies -->

**4. Ad-hoc Testing**

What ad-hoc testing was done? How are you convinced this change is correct (plots are good)?

**5. CI Testing**
<!-- Has the CI-testing been run? -->
- [ ] `!test repro` or `!test repro commit ` has been run

**6. Reproducibility**

Is this reproducible with the previous commit? (If not, why not?)
- [ ] Yes
- [ ] No

**7. Documentation**
<!--Does this impact documentation? Has the wiki been updated? Have the `docs/MOM_*` files been updated ?-->

The docs folder has been updated with output from running the model?
- [ ] Yes
- [ ] N/A

A PR has been created for updating the documentation?
- [ ] Yes: <!--link-->
- [ ] N/A

**8. Formatting**
<!-- Are changes to MOM_input in the same order as docs/MOM_parameter_docs.short? -->

Changes to MOM_input have been copied from model output in docs/MOM_parameter_docs.short?
- [ ] Yes
- [ ] N/A

**9. Merge Strategy**
<!-- What is the planned merge strategy (Merge commit, Rebase and merge, or squash) ?
If not squash, link to the related issue in the commit descriptions -->

- [ ] Merge commit
- [ ] Rebase and merge
- [ ] Squash
