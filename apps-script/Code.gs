/** @OnlyCurrentDoc */
/**
 * OCP Academy Feedback Survey — backend (Google Apps Script web app).
 * Saves each response as a row in the Google Sheet this script is attached to.
 *
 * 1. Edit CONFIG and FIELDS below if needed. Everything else can stay as it is.
 * 2. Run `setup` once (pick it in the toolbar, click Run, allow the permissions).
 * 3. Deploy → New deployment → Web app. Execute as: Me. Who has access: Anyone. Copy the /exec URL.
 * After ANY later change: Deploy → Manage deployments → pencil → Version: New version → Deploy.
 * Saving alone does not change the live form, and editing the existing deployment keeps the same URL.
 *
 * @OnlyCurrentDoc (line 1) limits the script to this one spreadsheet, which is what lets it
 * authorize under Google Advanced Protection. Keep sheetId '' so it uses the attached Sheet.
 */

// ---- 1. Settings ------------------------------------------------------------------------
const CONFIG = {
  title: 'OCP Academy Feedback Survey',
  intro: 'Enhancing your learning experience. Your feedback is crucial for improving the quality and relevance of the OCP Academy courses and materials. Fields marked * are required.',
  sheetId: '',              // '' = the Google Sheet this script was created from (Extensions → Apps Script)
  tab: 'Submissions',       // the tab rows go to; don't rename it once responses arrive
  refPrefix: 'ACAD',        // references look like ACAD-3F9A1C
  closes: '',               // no deadline: the survey stays open
  closesLabel: '',
  senderName: 'OCP Academy',  // name on the confirmation email (it is sent from the deploying account)
  replyTo: '',              // where replies to the confirmation go; '' = the deploying account
  sendReceipt: true,        // email the respondent a branded thank-you with a copy of their answers
  allowEdits: false,        // a survey: no edit link in the email
  notifyStaff: [],          // e.g. ['academy@opencompute.org']: emailed on every new response
  pageUrl: 'https://opencomputeproject.github.io/ocp-academy-courses/feedback/',  // the GitHub Pages page
  privacyUrl: 'https://www.opencompute.org/privacy',
  color: '#262673',         // OCP Academy indigo (from the logo)
  academyUrl: 'https://academy.opencompute.org/learn',
  rate: { perEmailPerHour: 5, allPerMinute: 20 },  // responses allowed
  staffColumns: ['Status', 'Notes'],               // reviewer columns after the answers; the form never writes them
  statusOptions: ['New', 'Reviewed', 'Follow up', 'Done'],
};

// ---- 2. Questions -----------------------------------------------------------------------
// type: text | email | url | textarea | select | radio | checkboxes | checkbox | date
// label = the Sheet column header. Labels match the old Google Form's response columns, so old
// and new responses line up. short = the shorter text shown on the page and in the email.
// section = a heading shown before the field. layout: 'scale' (1–10 buttons, ends = end labels)
// or 'row' (one row of a rating grid). ids: never change one once responses arrive.
const SCALE = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'];
const SAT = ['Not Satisfied', 'Extremely Satisfied'];
const RATE = ['Poor', 'Fair', 'Good', 'Excellent'];
const PREF = ['Least Prefer', 'Neutral', 'Highly Prefer'];
const MAT = 'Please rate the following aspects of the OCP Academy materials:';
const FMT = 'Which formats of content delivery did/do you prefer for technical learning?';
const row_ = (q, id, item, options, extra) =>
  Object.assign({ id, label: `${q} [${item}]`, short: item, type: 'radio', required: true, layout: 'row', options }, extra || {});

const FIELDS = [
  { id: 'email', label: 'Email Address', short: 'Email', type: 'email', required: true,
    section: { title: 'About you' } },
  { id: 'firstName', label: 'First name', type: 'text', required: true, max: 100 },
  { id: 'lastName', label: 'Last name', type: 'text', required: true, max: 100 },
  { id: 'heardFrom', label: 'How did you primarily come to know about the OCP Academy, in particular when you first signed up?',
    type: 'radio', required: true,
    options: ['OCP Summits or live events', 'OCP Biweekly Newsletter', 'OCP Community call (Project or Workstream)',
      'OCP Community mailing list (Project or Workstream)', 'OCP Website', 'Social Media', 'Word of mouth', 'Other'] },
  { id: 'heardOther', label: 'How did you hear about the OCP Academy? (Other)', short: 'If you chose Other, please tell us where',
    type: 'text', max: 200 },

  { id: 'satContent', label: "On a scale of 1 to 10, how satisfied are you overall with the OCP Academy's training content?",
    type: 'radio', required: true, layout: 'scale', options: SCALE, ends: SAT,
    section: { title: 'Overall satisfaction' } },
  { id: 'satPlatform', label: "On a scale of 1 to 10, how satisfied are you overall with the OCP Academy's website and platform?",
    type: 'radio', required: true, layout: 'scale', options: SCALE, ends: SAT },

  row_(MAT, 'matRelevance', 'Relevance to current industry needs', RATE,
    { section: { title: 'Course materials', text: 'Please rate the following aspects of the OCP Academy materials.' } }),
  row_(MAT, 'matClarity', 'Clarity and ease of understanding topics', RATE),
  row_(MAT, 'matDepth', 'Depth and technical rigor', RATE),
  row_(MAT, 'matExamples', 'Availability of practical examples/case studies', RATE),
  row_(MAT, 'matPresentation', 'Quality of presentation (videos, diagrams, reading, etc.)', RATE),
  row_(MAT, 'matQuizzes', 'Quality of knowledge checks (quizzes)', RATE),
  row_(MAT, 'matCourseNav', 'Course navigation or any technical issues', RATE),
  row_(MAT, 'matSiteNav', 'OCP Academy website navigation or any technical issues', RATE),
  { id: 'matComments', label: 'Optional commentary about the previous answers', short: 'Optional commentary about the materials',
    type: 'textarea', max: 2000 },

  row_(FMT, 'fmtAudio', 'Audio narration', PREF,
    { section: { title: 'Learning formats', text: 'Which formats of content delivery did/do you prefer for technical learning?' } }),
  row_(FMT, 'fmtVideo', 'Video Lectures', PREF),
  row_(FMT, 'fmtQuizzes', 'Interactive Quizzes/Exercises', PREF),
  row_(FMT, 'fmtDiagrams', 'Interactive Diagrams or Simulations', PREF),
  row_(FMT, 'fmtGuides', 'Downloadable Written Guides', PREF),
  row_(FMT, 'fmtReading', 'Inline Course Reading', PREF),
  { id: 'fmtComments', label: 'Optional commentary about the previous answers', short: 'Optional commentary about learning formats',
    type: 'textarea', max: 2000 },

  { id: 'recommend', label: 'How likely are you to recommend the OCP Academy to a colleague?',
    type: 'radio', required: true, layout: 'scale', options: SCALE, ends: ['Not likely', 'Extremely likely'],
    section: { title: 'Your experience' } },
  { id: 'mostValuable', label: 'What is the single most valuable aspect of the OCP Academy for you? (Optional)',
    short: 'What is the single most valuable aspect of the OCP Academy for you?', type: 'textarea', max: 2000 },
  { id: 'improve', label: 'What area of the OCP Academy do you think requires the most urgent improvement?  (Optional)',
    short: 'What area of the OCP Academy do you think requires the most urgent improvement?', type: 'textarea', max: 2000 },

  { id: 'ideasCommunity', label: 'For new courses or existing course extensions, what areas of the OCP Community orientation would you like to see covered?',
    type: 'textarea', max: 2000,
    section: { title: 'New course ideas (optional)', text: 'Share feedback on desired new content. You can also submit a detailed',
      link: { url: 'https://forms.gle/xEMpXQf2F8Kthpc28', text: 'course suggestion' } } },
  { id: 'ideasTech', label: 'For new courses or existing course extensions, what areas of the OCP Technologies would you like to see covered?',
    type: 'textarea', max: 2000 },
];

// ---- Everything below works as is ------------------------------------------------------

const MAX = { text: 200, email: 254, url: 500, textarea: 2000, select: 200, radio: 200, checkboxes: 2000, date: 10 };
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const ID_RE = /^[A-Za-z][A-Za-z0-9_]*$/;

/** Run once from the editor. Creates the tab, headers, formatting and the edit-link secret. */
function setup() {
  checkConfig_();
  const ss = book_();
  let sh = ss.getSheetByName(CONFIG.tab);
  if (!sh) {
    const first = ss.getSheets()[0];
    sh = (ss.getSheets().length === 1 && first.getLastRow() === 0) ? first.setName(CONFIG.tab) : ss.insertSheet(CONFIG.tab, 0);
  }
  if (sh.getLastRow() > 0) { Logger.log(`"${CONFIG.tab}" already has headers; left as is. ` + columnProblem_(sh)); return; }
  const h = headers_(), n = h.length, nAns = FIELDS.length + 2;
  sh.getRange(1, 1, 1, n).setValues([h]).setFontWeight('bold').setFontColor('#FFFFFF')
    .setBackground(CONFIG.color).setWrap(true).setVerticalAlignment('middle');
  sh.getRange(1, nAns + 2, 1, CONFIG.staffColumns.length).setBackground('#5F6062');
  sh.setFrozenRows(1); sh.setFrozenColumns(2);
  h.forEach((x, i) => sh.setColumnWidth(i + 1, i < 2 ? 140 : (FIELDS[i - 2] && FIELDS[i - 2].type === 'textarea') ? 360 : 180));
  const rows = sh.getMaxRows() - 1;
  sh.getRange(2, 1, rows, n).setVerticalAlignment('top').setWrap(true);
  sh.getRange(2, 1, rows, 1).setNumberFormat('yyyy-mm-dd hh:mm');
  sh.getRange(2, nAns + 1, rows, 1).setNumberFormat('yyyy-mm-dd hh:mm');
  if (CONFIG.staffColumns[0] && CONFIG.statusOptions.length)
    sh.getRange(2, nAns + 2, rows, 1).setDataValidation(SpreadsheetApp.newDataValidation()
      .requireValueInList(CONFIG.statusOptions, true).setAllowInvalid(false).build());
  editSecret_();
  Logger.log(`Set up "${CONFIG.tab}" in "${ss.getName()}". Next: Deploy → New deployment → Web app.`);
}

/** Run once after pasting a new version if Google asks for permissions. */
function authorize() {
  checkConfig_(); book_(); editSecret_();
  Logger.log('Permissions OK. Emails left today: ' + MailApp.getRemainingDailyQuota());
}

/** Checks that the Sheet's answer columns still match FIELDS (run it after changing the questions). */
function checkColumns() {
  checkConfig_();
  const sh = book_().getSheetByName(CONFIG.tab);
  Logger.log(sh ? columnProblem_(sh) || 'Columns match FIELDS.' : `No tab named "${CONFIG.tab}" yet: run setup.`);
}

/** Logs every submission's private edit link (to resend one by hand). Visible only to you in the log. */
function listEditLinks() {
  const sh = book_().getSheetByName(CONFIG.tab);
  if (!sh || sh.getLastRow() < 2) return;
  sh.getRange(2, 2, sh.getLastRow() - 1, 1).getValues().forEach(r => { if (r[0]) Logger.log(`${r[0]}  ${editLink_(r[0])}`); });
}

// ---- Web entry points. A function whose name does not end in _ can be called from a browser
// through google.script.run, so the editor tools above only log, and every new helper must end in _.
function doGet(e) {
  const p = (e && e.parameter) || {};
  if (p.action) return json_(apiGet(p));
  let out;
  try { out = HtmlService.createHtmlOutputFromFile('Form'); }
  catch (err) { return json_({ ok: false, error: 'This project has no Form page. Add an HTML file named Form.' }); }
  const boot = { edit: String(p.edit || ''), t: String(p.t || ''), config: publicConfig_() };
  // < is escaped so nothing in the address can close this script tag.
  out.append('<script>window.__BOOT__=' + JSON.stringify(boot).replace(/</g, '\\u003c') + ';</script>');
  return out.setTitle(CONFIG.title).addMetaTag('viewport', 'width=device-width, initial-scale=1');
}
function doPost(e) {
  let d;
  try { d = JSON.parse(e.postData.contents); } catch (err) { return json_({ ok: false, error: 'The submission could not be read.' }); }
  return json_(apiPost(d));
}
// Called by the page through google.script.run when Apps Script serves it, and by doGet/doPost otherwise.
function apiGet(p) {
  try {
    p = p || {};
    if (p.action === 'config') return { ok: true, config: publicConfig_() };
    if (p.action !== 'load') return { ok: false, error: 'Unknown request.' };
    if (!CONFIG.allowEdits || !p.ref || !tokenOk_(p.ref, p.t)) return { ok: false, error: 'This edit link is not valid.' };
    if (isClosed_()) return { ok: false, error: 'The deadline has passed, so this submission can no longer be edited.' };
    const sh = book_().getSheetByName(CONFIG.tab);
    const r = sh ? findRow_(sh, p.ref) : 0;
    if (!r) return { ok: false, error: 'We could not find this submission.' };
    const v = sh.getRange(r, 3, 1, FIELDS.length).getValues()[0];
    const data = {};
    FIELDS.forEach((f, i) => { data[f.id] = fromCell_(f, v[i]); });
    return { ok: true, ref: p.ref, data };
  } catch (err) {
    console.error(err);
    return { ok: false, error: 'Something went wrong on our side.' };
  }
}
function apiPost(d) {
  try {
    if (typeof d === 'string') d = JSON.parse(d);
    d = d || {};
    if (d.website) return { ok: true, ref: CONFIG.refPrefix + '-000000' };   // honeypot: bots fill the hidden field
    if (isClosed_()) return { ok: false, error: 'The deadline has passed.' };
    const editing = !!d.editRef;
    if (editing && (!CONFIG.allowEdits || !tokenOk_(d.editRef, d.editToken)))
      return { ok: false, error: 'This edit link is not valid.' };

    const clean = {};
    for (const f of FIELDS) {
      const res = check_(f, d[f.id]);
      if (res.error) return { ok: false, error: res.error, field: f.id };
      clean[f.id] = res.value;
    }

    const ref = editing ? String(d.editRef) : CONFIG.refPrefix + '-' + Utilities.getUuid().replace(/-/g, '').slice(0, 6).toUpperCase();
    const lock = LockService.getScriptLock();
    lock.waitLock(20000);
    try {
      const limited = rateLimited_(clean.email);
      if (limited) return limited;
      const ss = book_();
      const sh = ss.getSheetByName(CONFIG.tab);
      if (!sh || sh.getLastRow() === 0) return { ok: false, error: 'The form is not set up yet (run setup).' };
      // Never write answers into the wrong columns: the headers must match FIELDS exactly.
      const problem = columnProblem_(sh);
      if (problem) { console.error(problem); return { ok: false, error: 'The form is being updated. Please try again later.' }; }
      const answers = FIELDS.map(f => toCell_(f, clean[f.id]));
      if (editing) {
        const r = findRow_(sh, ref);
        if (!r) return { ok: false, error: 'We could not find this submission.' };
        sh.getRange(r, 3, 1, answers.length + 1).setValues([answers.concat([new Date()])]);  // answers + Last edited
      } else {
        const status = CONFIG.staffColumns[0] && CONFIG.statusOptions[0] ? [CONFIG.statusOptions[0]] : [];
        sh.getRange(nextRow_(sh), 1, 1, answers.length + 3 + status.length)
          .setValues([[new Date(), ref].concat(answers, [''], status)]);
      }
    } finally {
      lock.releaseLock();
    }

    // The row is saved; an email problem must not turn that into a failure for the submitter.
    if (CONFIG.sendReceipt) { try { sendReceipt_(clean, ref, editing); } catch (err) { console.error('Receipt failed: ' + err); } }
    if (!editing && CONFIG.notifyStaff.length) { try { notifyStaff_(clean, ref); } catch (err) { console.error('Staff email failed: ' + err); } }
    return { ok: true, ref };
  } catch (err) {
    console.error(err);
    return { ok: false, error: 'Something went wrong on our side.' };
  }
}

// ---- Validation (the browser checks too, but never trust it alone) ---------------------
function check_(f, raw) {
  const name = f.short || f.label;
  const req = msg => ({ error: msg || `"${name}" is required.` });
  if (f.type === 'checkbox') {
    const v = raw === true || raw === 'true' || raw === 'Yes';
    return f.required && !v ? req(`Please tick "${name}".`) : { value: v };
  }
  if (f.type === 'checkboxes') {
    const list = Array.isArray(raw) ? raw.map(String) : [];
    if (list.some(x => f.options.indexOf(x) < 0)) return { error: `"${name}" has an answer that is not one of the choices.` };
    if (f.required && !list.length) return req();
    return { value: list };
  }
  const v = String(raw == null ? '' : raw).trim();
  if (!v) return f.required ? req() : { value: '' };
  if (v.length > (f.max || MAX[f.type] || 200)) return { error: `"${name}" is over its ${f.max || MAX[f.type] || 200}-character limit.` };
  if (f.type === 'email' && !EMAIL_RE.test(v)) return { error: `"${name}" is not a valid email address.` };
  if (f.type === 'url' && !/^https?:\/\/\S+$/i.test(v)) return { error: `"${name}" must be a web address starting with http:// or https://.` };
  if (f.type === 'date' && !/^\d{4}-\d{2}-\d{2}$/.test(v)) return { error: `"${name}" is not a valid date.` };
  if ((f.type === 'select' || f.type === 'radio') && f.options.indexOf(v) < 0) return { error: `"${name}" is not one of the choices.` };
  return { value: v };
}

// ---- Formula injection and exact text ---------------------------------------------------
// Every typed answer is written with a leading apostrophe. Sheets then stores it exactly as typed:
// "=HYPERLINK(...)" stays text instead of running as a formula, "0123" keeps its zero, "1/2" stays
// text instead of becoming a date. The apostrophe is hidden in the Sheet and is not part of the value.
function toCell_(f, v) {
  if (f.type === 'checkbox') return v ? 'Yes' : 'No';
  if (f.type === 'checkboxes') v = v.join(', ');
  return v === '' ? '' : "'" + v;
}
function fromCell_(f, v) {
  if (f.type === 'checkbox') return v === 'Yes' || v === true;
  if (v instanceof Date) v = Utilities.formatDate(v, Session.getScriptTimeZone(), 'yyyy-MM-dd');
  v = String(v == null ? '' : v);
  if (v.charAt(0) === "'") v = v.slice(1);   // only if a Sheet ever returns the hidden apostrophe
  if (f.type === 'checkboxes') return v ? v.split(', ') : [];
  return v;
}

// ---- Rate limits: sliding windows in the script cache (entries expire on their own) -----
function rateLimited_(email) {
  const cache = CacheService.getScriptCache(), now = Date.now();
  const recent = (key, ms) => { let a = []; try { a = JSON.parse(cache.get(key) || '[]'); } catch (e) { a = []; } return a.filter(t => now - t < ms); };
  const all = recent('rl:all', 60000);
  if (all.length >= CONFIG.rate.allPerMinute) return { ok: false, error: "We're receiving a lot of submissions right now." };
  const key = 'rl:email:' + Utilities.base64EncodeWebSafe(Utilities.computeDigest(
    Utilities.DigestAlgorithm.SHA_256, String(email || '').trim().toLowerCase()));
  const mine = recent(key, 3600000);
  if (mine.length >= CONFIG.rate.perEmailPerHour) {
    const mins = Math.max(1, Math.ceil((Math.min.apply(null, mine) + 3600000 - now) / 60000));
    return { ok: false, limited: true, error: `This email address has reached the limit of ${CONFIG.rate.perEmailPerHour} submissions or edits in an hour. Please try again in about ${mins} minute${mins === 1 ? '' : 's'}.` };
  }
  all.push(now); mine.push(now);
  cache.put('rl:all', JSON.stringify(all), 120);
  cache.put(key, JSON.stringify(mine), 3600);
  return null;
}

// ---- Private edit links: ?edit=<reference>&t=<HMAC signature> -----------------------------
function editSecret_() {
  const props = PropertiesService.getScriptProperties();
  let s = props.getProperty('EDIT_SECRET');
  if (!s) { s = Utilities.getUuid() + Utilities.getUuid(); props.setProperty('EDIT_SECRET', s); }
  return s;
}
function editToken_(ref) {
  return Utilities.base64EncodeWebSafe(Utilities.computeHmacSha256Signature('edit|' + ref, editSecret_())).replace(/=+$/, '').slice(0, 32);
}
function tokenOk_(ref, t) {
  const want = editToken_(String(ref)), got = String(t || '');
  if (want.length !== got.length) return false;
  let diff = 0;
  for (let i = 0; i < want.length; i++) diff |= want.charCodeAt(i) ^ got.charCodeAt(i);   // constant time
  return diff === 0;
}
function editLink_(ref) {
  const base = CONFIG.pageUrl || ScriptApp.getService().getUrl();
  return base + (base.indexOf('?') < 0 ? '?' : '&') + 'edit=' + encodeURIComponent(ref) + '&t=' + editToken_(ref);
}

// ---- Emails (OCP Academy branding) ---------------------------------------------------------
// The logo is embedded in this script (LOGO_PNG_B64 at the end) and sent as an inline image, so
// the email needs no extra permission and works wherever the form is hosted.
const esc_ = v => String(v == null ? '' : v).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const shown_ = (f, v) => f.type === 'checkbox' ? (v ? 'Yes' : 'No') : f.type === 'checkboxes' ? v.join(', ') : v;
const BRAND = { indigo: '#262673', deep: '#19194D', green: '#8DC63F', gray: '#5F6062', line: '#DADCDF', paper: '#F3F4F5', body: '#3F4042' };

function answersHtml_(d) {
  return FIELDS.map(f => {
    const head = f.section ? `<tr><td colspan="2" style="padding:18px 0 6px;font:bold 11px/1.4 Arial,sans-serif;letter-spacing:2px;text-transform:uppercase;color:${BRAND.indigo};border-bottom:2px solid ${BRAND.green};">${esc_(f.section.title)}</td></tr>` : '';
    return head + `<tr><td style="padding:7px 14px 7px 0;color:${BRAND.gray};vertical-align:top;width:46%;border-bottom:1px solid ${BRAND.line};">${esc_(f.short || f.label)}</td>` +
      `<td style="padding:7px 0;color:${BRAND.deep};vertical-align:top;white-space:pre-wrap;border-bottom:1px solid ${BRAND.line};">${esc_(shown_(f, d[f.id])) || '—'}</td></tr>`;
  }).join('');
}
function answersText_(d) {
  return FIELDS.map(f => (f.section ? `\n${f.section.title.toUpperCase()}\n` : '') + `${f.short || f.label}: ${shown_(f, d[f.id]) || '—'}`).join('\n');
}

function sendReceipt_(d, ref, updated) {
  const link = CONFIG.allowEdits ? editLink_(ref) : '';
  const until = CONFIG.closesLabel ? ` until ${CONFIG.closesLabel}` : '';
  const head = updated ? 'Your feedback was updated' : 'Thank you for your feedback';
  const name = d.firstName ? `Hi ${esc_(d.firstName)},` : 'Hello,';
  const html = `<div style="background:#E9EBEF;padding:24px 12px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:600px;margin:0 auto;background:#FFFFFF;font:14px/1.6 Arial,sans-serif;color:${BRAND.body};border-collapse:collapse;">
<tr><td style="padding:20px 32px 16px;"><a href="${esc_(CONFIG.academyUrl)}" style="text-decoration:none;"><img src="cid:academyLogo" width="160" height="74" alt="OCP Academy" style="display:block;border:0;"></a></td></tr>
<tr><td style="background:${BRAND.indigo};padding:26px 32px 24px;border-bottom:6px solid ${BRAND.green};">
<div style="font:bold 11px/1.4 Arial,sans-serif;letter-spacing:3px;text-transform:uppercase;color:${BRAND.green};">${esc_(CONFIG.title)}</div>
<div style="font:bold 24px/1.25 'Franklin Gothic Medium','Arial Narrow',Arial,sans-serif;letter-spacing:1px;color:#FFFFFF;margin-top:8px;">${head}</div></td></tr>
<tr><td style="padding:26px 32px 4px;"><p style="margin:0 0 12px;">${name}</p>
<p style="margin:0 0 12px;">${updated ? 'Your changes are saved.' : 'Thank you for taking the time to share your experience with the OCP Academy. Your feedback helps us improve our courses and decide what to build next.'}</p>
<p style="margin:0;">Your reference is <b style="color:${BRAND.deep};">${esc_(ref)}</b>. Here is a copy of your answers:</p></td></tr>
<tr><td style="padding:4px 32px 8px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="font:13px/1.5 Arial,sans-serif;border-collapse:collapse;">${answersHtml_(d)}</table></td></tr>
${link ? `<tr><td style="padding:16px 32px 8px;"><p style="margin:0 0 12px;">Need to change something? You can edit your answers${esc_(until)}.</p>
<a href="${esc_(link)}" style="display:inline-block;background:${BRAND.green};color:${BRAND.deep};font:bold 13px Arial,sans-serif;letter-spacing:1px;text-transform:uppercase;text-decoration:none;padding:12px 20px;border-radius:4px;">Edit your answers</a>
<p style="margin:10px 0 0;font-size:12px;color:${BRAND.gray};">This link is private to your response. Please don't forward it.</p></td></tr>` : ''}
<tr><td style="padding:22px 32px 28px;"><a href="${esc_(CONFIG.academyUrl)}" style="display:inline-block;background:${BRAND.green};color:${BRAND.deep};font:bold 13px Arial,sans-serif;letter-spacing:1px;text-transform:uppercase;text-decoration:none;padding:12px 20px;border-radius:4px;">Explore OCP Academy courses</a></td></tr>
<tr><td style="background:${BRAND.paper};padding:18px 32px;font:12px/1.6 Arial,sans-serif;color:${BRAND.gray};border-top:1px solid ${BRAND.line};">Open Compute Project Foundation · <a href="${esc_(CONFIG.academyUrl)}" style="color:${BRAND.indigo};">OCP Academy</a>${CONFIG.privacyUrl ? ` · <a href="${esc_(CONFIG.privacyUrl)}" style="color:${BRAND.indigo};">Privacy policy</a>` : ''}<br>You are receiving this because this address was entered on the OCP Academy feedback survey.</td></tr></table></div>`;
  const text = `${head}\nReference: ${ref}\n\nThank you for taking the time to share your experience with the OCP Academy.\n${answersText_(d)}\n` +
    (link ? `\nEdit your answers${until}:\n${link}\n(This link is private to your response. Please don't forward it.)\n` : '') +
    `\nExplore OCP Academy courses: ${CONFIG.academyUrl}\n`;
  const mail = { to: d.email, subject: `${updated ? 'Updated' : 'Thank you'}: your OCP Academy feedback (${ref})`, body: text, htmlBody: html,
    name: CONFIG.senderName, inlineImages: { academyLogo: logoBlob_() } };
  if (CONFIG.replyTo) mail.replyTo = CONFIG.replyTo;
  MailApp.sendEmail(mail);
}

function notifyStaff_(d, ref) {
  const book = book_();
  MailApp.sendEmail({
    to: CONFIG.notifyStaff.join(','), name: CONFIG.senderName, replyTo: d.email,
    subject: `New response: ${CONFIG.title} (${ref})`,
    body: `${answersText_(d)}\n\nSheet: ${book.getUrl()}`,
    htmlBody: `<div style="font:14px/1.6 Arial,sans-serif;color:${BRAND.body};"><p>New response <b>${esc_(ref)}</b>.</p><table style="border-collapse:collapse;">${answersHtml_(d)}</table><p><a href="${esc_(book.getUrl())}">Open the Sheet</a></p></div>`,
  });
}
function logoBlob_() { return Utilities.newBlob(Utilities.base64Decode(LOGO_PNG_B64), 'image/png', 'ocp-academy.png'); }

// ---- Sheet helpers ------------------------------------------------------------------------
function book_() { return CONFIG.sheetId ? SpreadsheetApp.openById(CONFIG.sheetId) : SpreadsheetApp.getActiveSpreadsheet(); }
function headers_() { return ['Submitted', 'Reference'].concat(FIELDS.map(f => f.label), ['Last edited'], CONFIG.staffColumns); }
// '' when columns A..(Last edited) match FIELDS; otherwise what differs. Staff column names are free.
function columnProblem_(sh) {
  const want = headers_().slice(0, FIELDS.length + 3);
  const have = sh.getRange(1, 1, 1, want.length).getValues()[0].map(String);
  const diffs = want.map((w, i) => w === have[i] ? '' : `column ${i + 1}: Sheet has "${have[i]}", FIELDS expects "${w}"`).filter(String);
  return diffs.length ? 'Columns do not match FIELDS: ' + diffs.join('; ') +
    '. Fix the Sheet header (or FIELDS) so they match, then run checkColumns.' : '';
}
function findRow_(sh, ref) {
  const last = sh.getLastRow();
  if (last < 2) return 0;
  const refs = sh.getRange(2, 2, last - 1, 1).getValues();
  for (let i = 0; i < refs.length; i++) if (String(refs[i][0]) === String(ref)) return i + 2;
  return 0;
}
// The row after the last reference (checkbox or dropdown cells can make getLastRow() point further down).
function nextRow_(sh) {
  const max = sh.getMaxRows();
  const refs = max > 1 ? sh.getRange(2, 2, max - 1, 1).getValues() : [];
  let last = 1;
  for (let i = refs.length - 1; i >= 0; i--) if (refs[i][0] !== '') { last = i + 2; break; }
  if (last + 1 > max) sh.insertRowsAfter(max, 100);
  return last + 1;
}
const isClosed_ = () => !!CONFIG.closes && new Date() > new Date(CONFIG.closes);
function publicConfig_() {
  return {
    title: CONFIG.title, intro: CONFIG.intro, closes: CONFIG.closes, closesLabel: CONFIG.closesLabel,
    allowEdits: CONFIG.allowEdits, sendReceipt: CONFIG.sendReceipt, privacyUrl: CONFIG.privacyUrl, color: CONFIG.color,
    fields: FIELDS.map(f => ({ id: f.id, label: f.short || f.label, type: f.type, required: !!f.required, options: f.options || null,
      help: f.help || '', placeholder: f.placeholder || '', max: f.max || MAX[f.type] || 200,
      layout: f.layout || '', ends: f.ends || null, section: f.section || null })),
  };
}
function checkConfig_() {
  const seen = {};
  FIELDS.forEach(f => {
    if (!ID_RE.test(f.id || '')) throw new Error(`Field id "${f.id}" must start with a letter and use only letters, digits and _.`);
    if (seen[f.id]) throw new Error(`Field id "${f.id}" is used twice.`);
    seen[f.id] = true;
    if (!MAX[f.type] && f.type !== 'checkbox') throw new Error(`Field "${f.id}" has an unknown type "${f.type}".`);
    if (['select', 'radio', 'checkboxes'].indexOf(f.type) >= 0 && !(f.options && f.options.length)) throw new Error(`Field "${f.id}" needs options.`);
  });
  if (!FIELDS.some(f => f.id === 'email' && f.type === 'email')) throw new Error('FIELDS needs one field with id "email" and type "email".');
  if (seen.website || seen.editRef || seen.editToken || seen.action) throw new Error('Field ids website, editRef, editToken and action are reserved.');
}
function json_(obj) { return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON); }

// OCP Academy logo (PNG, 400×185) for the confirmation email.
const LOGO_PNG_B64 = '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';
