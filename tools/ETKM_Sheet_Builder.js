/**
 * ETKM COLD EMAIL DATABASE — MASTER SHEET BUILDER
 * Version: 1.0 | March 2026
 * 
 * HOW TO RUN:
 * 1. Go to script.google.com
 * 2. Click "New Project"
 * 3. Delete any existing code in the editor
 * 4. Paste this entire script
 * 5. Click Save (Ctrl+S or Cmd+S) — name it "ETKM Sheet Builder"
 * 6. Click Run (▶) — make sure buildETKMMasterSheet is selected in the dropdown
 * 7. Approve permissions when prompted (it needs to create a Google Sheet)
 * 8. When complete, the script will show you the Sheet URL in the Logs
 *    (View > Logs, or Ctrl+Enter)
 * 
 * WHAT IT BUILDS:
 * - New Google Sheet named "ETKM Cold Email Database — Master"
 * - 13 tabs in correct order
 * - 16-column header structure on all cold email tabs
 * - Status dropdown validation (Column K) on all cold email tabs
 * - Audit_Log tab with its own column structure
 * - Pending_Review tab with its own column structure
 * - Relationships tab with its own column structure
 * - ETKM brand formatting (black header, white text, red accent column)
 * - Frozen header row on all tabs
 * - Column widths optimized for readability
 * - One test row in the LE tab (uses your own email — update before running)
 * - First Audit_Log entry recording the Sheet creation
 */

// ─────────────────────────────────────────────
// CONFIGURATION — UPDATE BEFORE RUNNING
// ─────────────────────────────────────────────
var CONFIG = {
  // The email address Make.com will use — add as a viewer/editor after creation
  makeComEmail: 'YOUR_MAKECOM_GOOGLE_ACCOUNT@gmail.com',
  
  // Your email for the test row in the LE tab
  testEmail: 'easttxkravmaga@gmail.com',
  
  // Your name — appears in the first Audit_Log entry
  ownerName: 'Nathan Lundstrom'
};

// ─────────────────────────────────────────────
// BRAND COLORS
// ─────────────────────────────────────────────
var COLORS = {
  black:      '#000000',
  white:      '#FFFFFF',
  red:        '#CC0000',   // Slightly dimmed red — Google Sheets renders FF0000 very bright
  gray:       '#575757',
  litegray:   '#BBBBBB',
  surface:    '#1a1a1a',
  autoCol:    '#1a2a1a',   // Dark green tint for auto-populated columns
  autoText:   '#5aad5a',
  reqCol:     '#1a1a00',   // Dark yellow tint for required columns
  headerBg:   '#000000',
  altRow:     '#0d0d0d'
};

// ─────────────────────────────────────────────
// COLUMN DEFINITIONS — COLD EMAIL TABS
// ─────────────────────────────────────────────
var COLD_EMAIL_HEADERS = [
  { name: 'first_name',           type: 'required',  width: 120, note: 'Required. Real first name only — not Office or Contact.' },
  { name: 'last_name',            type: 'optional',  width: 120, note: 'Include if known.' },
  { name: 'email',                type: 'required',  width: 220, note: 'Required. Individual email preferred over info@.' },
  { name: 'organization',         type: 'required',  width: 240, note: 'Required. Exact org name — match master org list.' },
  { name: 'title',                type: 'required',  width: 200, note: 'Required. Their actual job title.' },
  { name: 'city',                 type: 'required',  width: 110, note: 'Required. City where the org is located.' },
  { name: 'segment',              type: 'required',  width: 160, note: 'Required. Must match this tab name exactly.' },
  { name: 'email_1_sent',         type: 'auto',      width: 110, note: 'AUTO — Make writes date after Email 1 sends. Leave blank.' },
  { name: 'email_2_sent',         type: 'auto',      width: 110, note: 'AUTO — Make writes date after Email 2 sends. Leave blank.' },
  { name: 'email_3_sent',         type: 'auto',      width: 110, note: 'AUTO — Make writes date after Email 3 sends. Leave blank.' },
  { name: 'status',               type: 'required',  width: 110, note: 'Required. Use dropdown only — no free text.' },
  { name: 'notes',                type: 'optional',  width: 260, note: 'Optional. Reply context, flags, how contact was found.' },
  { name: 'sequence_start_date',  type: 'auto',      width: 140, note: 'AUTO — Make writes when sequence begins. Leave blank.' },
  { name: 'source',               type: 'required',  width: 160, note: 'Required. Source tag: ORIGINAL_LIST, MANUAL_RESEARCH, REFERRAL, EVENT, INBOUND, GOOGLE_MAPS, CHAMBER_DIRECTORY, ISD_WEBSITE, LE_DIRECTORY' },
  { name: 'date_added',           type: 'required',  width: 110, note: 'Required. Date this row was added.' },
  { name: 'last_verified',        type: 'required',  width: 110, note: 'Required. Date contact info was last confirmed accurate.' }
];

var STATUS_VALUES = [
  'active',
  'replied',
  'opted_out',
  'bounced',
  'hold',
  'converted',
  'no_contact'
];

var SOURCE_VALUES = [
  'ORIGINAL_LIST',
  'MANUAL_RESEARCH',
  'REFERRAL',
  'EVENT',
  'INBOUND',
  'GOOGLE_MAPS',
  'CHAMBER_DIRECTORY',
  'ISD_WEBSITE',
  'LE_DIRECTORY'
];

// ─────────────────────────────────────────────
// TAB DEFINITIONS
// ─────────────────────────────────────────────
var COLD_EMAIL_TABS = [
  { name: 'LE',                      label: 'Law Enforcement',              color: '#CC0000' },
  { name: 'Fire_EMS',                label: 'Fire / EMS',                   color: '#CC4400' },
  { name: 'Churches_Security',       label: 'Churches — Security',          color: '#884400' },
  { name: 'Churches_Womens',         label: 'Churches — Women\'s',          color: '#884400' },
  { name: 'Churches_Youth',          label: 'Churches — Youth',             color: '#884400' },
  { name: 'Private_Schools',         label: 'Private / Christian Schools',  color: '#446600' },
  { name: 'Homeschool',              label: 'Homeschool Groups',            color: '#446600' },
  { name: 'Public_ISD',              label: 'Public ISDs',                  color: '#446600' },
  { name: 'Colleges',                label: 'Colleges & Universities',      color: '#224466' },
  { name: 'Employers_Professionals', label: 'Large Employers & Professionals', color: '#224466' }
];

// ─────────────────────────────────────────────
// MAIN FUNCTION — RUN THIS
// ─────────────────────────────────────────────
function buildETKMMasterSheet() {
  Logger.log('=== ETKM Master Sheet Builder Starting ===');
  Logger.log('Building: ETKM Cold Email Database — Master');
  
  // Create the spreadsheet
  var ss = SpreadsheetApp.create('ETKM Cold Email Database — Master');
  var url = ss.getUrl();
  Logger.log('Sheet created: ' + url);
  
  // Rename the default Sheet1
  var defaultSheet = ss.getSheets()[0];
  defaultSheet.setName('LE');
  
  // ── BUILD ALL COLD EMAIL TABS ──
  Logger.log('Building cold email tabs...');
  
  // LE tab already exists — set it up first
  buildColdEmailTab(ss, defaultSheet, COLD_EMAIL_TABS[0]);
  
  // Create the remaining 9 cold email tabs
  for (var i = 1; i < COLD_EMAIL_TABS.length; i++) {
    var sheet = ss.insertSheet(COLD_EMAIL_TABS[i].name);
    buildColdEmailTab(ss, sheet, COLD_EMAIL_TABS[i]);
    Logger.log('Tab built: ' + COLD_EMAIL_TABS[i].name);
    SpreadsheetApp.flush();
  }
  
  // ── BUILD RELATIONSHIPS TAB ──
  Logger.log('Building Relationships tab...');
  var relSheet = ss.insertSheet('Relationships');
  buildRelationshipsTab(relSheet);
  
  // ── BUILD AUDIT_LOG TAB ──
  Logger.log('Building Audit_Log tab...');
  var auditSheet = ss.insertSheet('Audit_Log');
  buildAuditLogTab(auditSheet);
  
  // ── BUILD PENDING_REVIEW TAB ──
  Logger.log('Building Pending_Review tab...');
  var pendingSheet = ss.insertSheet('Pending_Review');
  buildPendingReviewTab(pendingSheet);
  
  // ── ADD TEST ROW TO LE TAB ──
  Logger.log('Adding test row to LE tab...');
  addTestRow(ss.getSheetByName('LE'));
  
  // ── FIRST AUDIT LOG ENTRY ──
  Logger.log('Writing first Audit_Log entry...');
  var auditLog = ss.getSheetByName('Audit_Log');
  writeAuditEntry(auditLog, [
    formatDate(new Date()),
    'SHEET_CREATED',
    'ALL',
    'N/A',
    'N/A',
    'Master Sheet built by Google Apps Script. All 13 tabs created. Test row added to LE tab. Ready for contact population.',
    CONFIG.ownerName
  ]);
  
  // ── PROTECT HEADER ROWS ──
  Logger.log('Protecting header rows...');
  protectHeaders(ss);
  
  // ── SHARE WITH MAKE ──
  if (CONFIG.makeComEmail && CONFIG.makeComEmail !== 'YOUR_MAKECOM_GOOGLE_ACCOUNT@gmail.com') {
    Logger.log('Sharing with Make.com account...');
    try {
      ss.addEditor(CONFIG.makeComEmail);
      Logger.log('Shared with: ' + CONFIG.makeComEmail);
    } catch(e) {
      Logger.log('Could not share automatically — share manually with: ' + CONFIG.makeComEmail);
    }
  }
  
  // ── REORDER TABS (move Audit_Log and Pending_Review to end) ──
  // Already in correct order since we built them in sequence
  
  // ── DONE ──
  Logger.log('');
  Logger.log('=== BUILD COMPLETE ===');
  Logger.log('Sheet URL: ' + url);
  Logger.log('');
  Logger.log('NEXT STEPS:');
  Logger.log('1. Open the Sheet at the URL above');
  Logger.log('2. Go to the LE tab — verify the test row is there');
  Logger.log('3. Share the Sheet with your Make.com Google account (Editor access)');
  Logger.log('4. Save this Sheet URL in your Make.com Google Sheets connection');
  Logger.log('5. Begin populating the LE tab with real contacts');
  Logger.log('');
  Logger.log('Test row email is set to: ' + CONFIG.testEmail);
  Logger.log('Update testEmail in CONFIG before populating real contacts.');
  
  // Show a dialog with the URL
  try {
    SpreadsheetApp.getUi().alert(
      'ETKM Master Sheet Built Successfully!\n\n' +
      'URL: ' + url + '\n\n' +
      'Open the Sheet and verify the LE tab test row.\n' +
      'Then share with your Make.com Google account.'
    );
  } catch(e) {
    // Script editor doesn't have UI — URL is in Logs
  }
  
  return url;
}

// ─────────────────────────────────────────────
// BUILD A COLD EMAIL TAB
// ─────────────────────────────────────────────
function buildColdEmailTab(ss, sheet, tabDef) {
  // Set tab color
  sheet.setTabColor(tabDef.color);
  
  // Write headers
  var headerRow = COLD_EMAIL_HEADERS.map(function(col) { return col.name; });
  sheet.getRange(1, 1, 1, headerRow.length).setValues([headerRow]);
  
  // Style the header row
  var headerRange = sheet.getRange(1, 1, 1, headerRow.length);
  headerRange.setBackground(COLORS.black);
  headerRange.setFontColor(COLORS.white);
  headerRange.setFontFamily('Arial');
  headerRange.setFontSize(10);
  headerRange.setFontWeight('bold');
  headerRange.setVerticalAlignment('middle');
  headerRange.setWrapStrategy(SpreadsheetApp.WrapStrategy.CLIP);
  
  // Color-code columns by type
  for (var i = 0; i < COLD_EMAIL_HEADERS.length; i++) {
    var col = COLD_EMAIL_HEADERS[i];
    var cell = sheet.getRange(1, i + 1);
    
    if (col.type === 'auto') {
      cell.setBackground('#1a2600');
      cell.setFontColor('#88cc44');
    } else if (col.type === 'optional') {
      cell.setBackground('#1a1a1a');
      cell.setFontColor(COLORS.litegray);
    } else {
      // required — white text on black (default)
    }
    
    // Add note to header cell
    cell.setNote(col.note);
    
    // Set column width
    sheet.setColumnWidth(i + 1, col.width);
  }
  
  // Red accent on column A header only
  sheet.getRange(1, 1).setBackground(COLORS.red).setFontColor(COLORS.white);
  
  // Freeze the header row
  sheet.setFrozenRows(1);
  
  // Freeze first 3 columns (name + email + org always visible)
  sheet.setFrozenColumns(3);
  
  // Add label row (row 2) with a subtitle showing tab purpose
  var labelRow = sheet.getRange(2, 1, 1, headerRow.length);
  labelRow.setBackground('#0d0d0d');
  labelRow.setFontColor(COLORS.gray);
  labelRow.setFontSize(9);
  labelRow.setFontStyle('italic');
  labelRow.setValues([[
    tabDef.label + ' — active contacts only',
    '', '', '', '', '', '',
    'AUTO', 'AUTO', 'AUTO',
    'dropdown', 'manual notes', 'AUTO',
    'source tag', 'today', 'today'
  ]]);
  
  // Freeze the label row too
  sheet.setFrozenRows(2);
  
  // Set default row height
  sheet.setDefaultRowHeight(24);
  
  // Apply status dropdown validation to the entire status column (K = column 11)
  // Start at row 3 to skip header and label rows, go to row 1000
  var statusRange = sheet.getRange(3, 11, 998, 1);
  var statusRule = SpreadsheetApp.newDataValidation()
    .requireValueInList(STATUS_VALUES, true)
    .setAllowInvalid(false)
    .setHelpText('Select a status from the dropdown. Do not type free text.')
    .build();
  statusRange.setDataValidation(statusRule);
  statusRange.setBackground('#0d0d0d');
  
  // Apply source dropdown validation to source column (N = column 14)
  var sourceRange = sheet.getRange(3, 14, 998, 1);
  var sourceRule = SpreadsheetApp.newDataValidation()
    .requireValueInList(SOURCE_VALUES, true)
    .setAllowInvalid(false)
    .setHelpText('Select a source tag from the dropdown.')
    .build();
  sourceRange.setDataValidation(sourceRule);
  
  // Alternate row banding — light and dark
  var banding = sheet.getRange(3, 1, 998, headerRow.length);
  try {
    var bandingObj = banding.applyRowBanding(SpreadsheetApp.BandingTheme.LIGHT_GREY);
    bandingObj.setHeaderRowColor(COLORS.black);
    bandingObj.setFirstRowColor('#111111');
    bandingObj.setSecondRowColor('#0d0d0d');
    bandingObj.setFooterRowColor(null);
  } catch(e) {
    // Banding may not be available in all contexts — skip gracefully
  }
  
  // Set date format on email_sent columns (H, I, J = 8, 9, 10)
  var dateFormat = 'yyyy-mm-dd';
  sheet.getRange(3, 8, 998, 3).setNumberFormat(dateFormat);
  // Also date format on date_added and last_verified (O, P = 15, 16)
  sheet.getRange(3, 15, 998, 2).setNumberFormat(dateFormat);
  // sequence_start_date (M = 13)
  sheet.getRange(3, 13, 998, 1).setNumberFormat(dateFormat);
  
  // Lock auto-populated columns with a note (don't use full protection — too restrictive)
  // Just make them visually distinct via the header color coding above
  
  // Set row 2 height shorter (it's just a label)
  sheet.setRowHeight(2, 18);
}

// ─────────────────────────────────────────────
// ADD TEST ROW TO LE TAB
// ─────────────────────────────────────────────
function addTestRow(sheet) {
  var today = formatDate(new Date());
  var testData = [
    'TEST',                          // first_name
    'ROW',                           // last_name
    CONFIG.testEmail,                // email
    'East Texas Krav Maga (TEST)',   // organization
    'Owner / Instructor',            // title
    'Tyler',                         // city
    'LE',                            // segment
    '',                              // email_1_sent — BLANK
    '',                              // email_2_sent — BLANK
    '',                              // email_3_sent — BLANK
    'hold',                          // status — hold so it never triggers Make
    'TEST ROW — verify Make sends to this row, then delete before going live',  // notes
    '',                              // sequence_start_date — BLANK
    'ORIGINAL_LIST',                 // source
    today,                           // date_added
    today                            // last_verified
  ];
  
  var testRow = sheet.getRange(3, 1, 1, testData.length);
  testRow.setValues([testData]);
  
  // Style the test row so it's unmissable
  testRow.setBackground('#3d1a00');
  testRow.setFontColor('#ff8c00');
  testRow.setFontWeight('bold');
  
  // Note on the row
  sheet.getRange(3, 1).setNote(
    'TEST ROW — For Make.com scenario testing only.\n\n' +
    'TO TEST:\n' +
    '1. Change status from "hold" to "active"\n' +
    '2. Run Make Scenario 1 — Email 1 should arrive at ' + CONFIG.testEmail + '\n' +
    '3. Verify email_1_sent populates with today\'s date\n' +
    '4. Set email_1_sent to 6 days ago → Run Scenario 2 → Verify Email 2\n' +
    '5. Set email_1_sent to 13 days ago → Run Scenario 3 → Verify Email 3\n' +
    '6. Set status to "opted_out" → Run all 3 → Verify NO emails send\n' +
    '7. After all tests pass: DELETE THIS ROW before going live'
  );
}

// ─────────────────────────────────────────────
// BUILD RELATIONSHIPS TAB
// ─────────────────────────────────────────────
function buildRelationshipsTab(sheet) {
  sheet.setTabColor('#444444');
  
  var headers = [
    'organization', 'category', 'strategy_tag', 'primary_contact',
    'contact_email', 'city', 'status', 'notes', 'last_contact_date', 'date_added'
  ];
  
  var widths = [240, 140, 160, 180, 200, 110, 110, 260, 130, 110];
  
  sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
  var headerRange = sheet.getRange(1, 1, 1, headers.length);
  headerRange.setBackground(COLORS.gray);
  headerRange.setFontColor(COLORS.white);
  headerRange.setFontFamily('Arial');
  headerRange.setFontSize(10);
  headerRange.setFontWeight('bold');
  
  for (var i = 0; i < widths.length; i++) {
    sheet.setColumnWidth(i + 1, widths[i]);
  }
  
  sheet.setFrozenRows(1);
  
  // Label row
  sheet.getRange(2, 1).setValue('NOT cold email targets — see notes for warm outreach strategy');
  sheet.getRange(2, 1, 1, headers.length).setBackground('#111111').setFontColor(COLORS.gray).setFontSize(9).setFontStyle('italic');
  sheet.setFrozenRows(2);
  
  // Strategy tag dropdown
  var strategyRange = sheet.getRange(3, 3, 998, 1);
  var strategyRule = SpreadsheetApp.newDataValidation()
    .requireValueInList(['REMOVE', 'RESOURCES_SEMINARS', 'SAFETY_COMMUNICATION', 'PR_RELATIONSHIP'], true)
    .setAllowInvalid(false)
    .build();
  strategyRange.setDataValidation(strategyRule);
  
  // Status dropdown (limited for relationship tab)
  var statusRange = sheet.getRange(3, 7, 998, 1);
  var statusRule = SpreadsheetApp.newDataValidation()
    .requireValueInList(['no_contact', 'contacted', 'active_relationship', 'dormant'], true)
    .setAllowInvalid(false)
    .build();
  statusRange.setDataValidation(statusRule);
  
  // Pre-populate with competitor entries (REMOVE — these should never change)
  var competitors = [
    ['Tiger-Rock Martial Arts of Tyler',    'Competitor', 'REMOVE', '', '', 'Tyler', 'no_contact', 'PERMANENT — Direct competitor. No contact ever.', '', formatDate(new Date())],
    ['Gracie Barra Tyler BJJ',              'Competitor', 'REMOVE', '', '', 'Tyler', 'no_contact', 'PERMANENT — Direct competitor. No contact ever.', '', formatDate(new Date())],
    ['Relson Gracie / Lone Star MMA Academy','Competitor', 'REMOVE', '', '', 'Tyler', 'no_contact', 'PERMANENT — Direct competitor. No contact ever.', '', formatDate(new Date())],
    ['Tyler Kung Fu & Fitness',             'Competitor', 'REMOVE', '', '', 'Tyler', 'no_contact', 'PERMANENT — Direct competitor. No contact ever.', '', formatDate(new Date())]
  ];
  
  sheet.getRange(3, 1, competitors.length, competitors[0].length).setValues(competitors);
  
  // Style competitor rows in dark red
  sheet.getRange(3, 1, 4, headers.length)
    .setBackground('#1a0000')
    .setFontColor('#ff6666');
  
  sheet.setDefaultRowHeight(24);
  sheet.setRowHeight(2, 18);
}

// ─────────────────────────────────────────────
// BUILD AUDIT_LOG TAB
// ─────────────────────────────────────────────
function buildAuditLogTab(sheet) {
  sheet.setTabColor('#333333');
  
  var headers = ['date', 'action_tag', 'tab_affected', 'org_name', 'contact_name', 'detail', 'who'];
  var widths   = [100,    180,          140,            220,        160,            380,     120];
  
  sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
  var headerRange = sheet.getRange(1, 1, 1, headers.length);
  headerRange.setBackground(COLORS.black);
  headerRange.setFontColor(COLORS.litegray);
  headerRange.setFontFamily('Arial');
  headerRange.setFontSize(10);
  headerRange.setFontWeight('bold');
  
  for (var i = 0; i < widths.length; i++) {
    sheet.setColumnWidth(i + 1, widths[i]);
  }
  
  sheet.setFrozenRows(1);
  
  // Note on this tab
  sheet.getRange(1, 1).setNote(
    'AUDIT LOG — Append-only.\n\n' +
    'NEVER delete a row from this tab.\n' +
    'NEVER edit a row after it has been written.\n\n' +
    'This is the permanent record of every change made to the database.\n\n' +
    'ACTION TAG VALUES:\n' +
    'ADDED / OPTED_OUT / BOUNCED / REPLIED / CONVERTED\n' +
    'BATCH_ADDED / SEGMENT_ASSIGNED / DUPLICATE_RESOLVED\n' +
    'CONTACT_CHANGED / ORG_CLOSED / ORG_MERGED / MAKE_ERROR\n' +
    'WEEKLY_METRICS / MONTHLY_REVIEW / MONTHLY_INFRA\n' +
    'QUARTERLY_ACCURACY / QUARTERLY_RELATIONSHIP / QUARTERLY_TAXONOMY\n' +
    'ANNUAL_VERIFY / ANNUAL_DEDUPE / ANNUAL_BACKUP / SHEET_CREATED'
  );
  
  sheet.setDefaultRowHeight(24);
}

// ─────────────────────────────────────────────
// BUILD PENDING_REVIEW TAB
// ─────────────────────────────────────────────
function buildPendingReviewTab(sheet) {
  sheet.setTabColor('#884400');
  
  var headers = [
    'first_name', 'last_name', 'email', 'organization', 'title', 'city',
    'why_pending', 'segment_guess', 'date_added', 'assigned_to', 'resolved_date'
  ];
  var widths = [120, 120, 220, 240, 200, 110, 280, 160, 110, 140, 110];
  
  sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
  var headerRange = sheet.getRange(1, 1, 1, headers.length);
  headerRange.setBackground('#7a3a00');
  headerRange.setFontColor(COLORS.white);
  headerRange.setFontFamily('Arial');
  headerRange.setFontSize(10);
  headerRange.setFontWeight('bold');
  
  for (var i = 0; i < widths.length; i++) {
    sheet.setColumnWidth(i + 1, widths[i]);
  }
  
  sheet.setFrozenRows(1);
  
  // Label row
  sheet.getRange(2, 1).setValue('Contacts with missing fields or unconfirmed segment — resolve at each monthly audit');
  sheet.getRange(2, 1, 1, headers.length)
    .setBackground('#1a0d00')
    .setFontColor('#ff8c00')
    .setFontSize(9)
    .setFontStyle('italic');
  sheet.setFrozenRows(2);
  
  sheet.setDefaultRowHeight(24);
  sheet.setRowHeight(2, 18);
  
  // Note on this tab
  sheet.getRange(1, 1).setNote(
    'PENDING REVIEW TAB\n\n' +
    'Contacts go here when:\n' +
    '- A required field is missing (no email, no first name, etc.)\n' +
    '- The correct segment is unclear\n' +
    '- The contact role is uncertain (Tier 3 or 4?)\n\n' +
    'WHY_PENDING column: explain exactly what is missing or unclear.\n' +
    'SEGMENT_GUESS column: your best guess before confirming.\n\n' +
    'Review and resolve at every monthly audit.\n' +
    'Move resolved contacts to correct segment tab.\n' +
    'Log the resolution in Audit_Log.'
  );
}

// ─────────────────────────────────────────────
// WRITE AN AUDIT LOG ENTRY
// ─────────────────────────────────────────────
function writeAuditEntry(auditSheet, rowData) {
  var lastRow = auditSheet.getLastRow();
  var targetRow = Math.max(lastRow + 1, 2); // Start at row 2 (below header)
  auditSheet.getRange(targetRow, 1, 1, rowData.length).setValues([rowData]);
  
  // Style the first entry
  if (targetRow === 2) {
    auditSheet.getRange(targetRow, 1, 1, rowData.length)
      .setBackground('#0d1a0d')
      .setFontColor(COLORS.green_text || '#5aad5a');
  }
}

// ─────────────────────────────────────────────
// PROTECT HEADER ROWS (soft protection with warning)
// ─────────────────────────────────────────────
function protectHeaders(ss) {
  var sheets = ss.getSheets();
  sheets.forEach(function(sheet) {
    try {
      var protection = sheet.getRange(1, 1, 2, sheet.getLastColumn() || 16).protect();
      protection.setDescription('Header rows — do not edit');
      protection.setWarningOnly(true); // Warning, not hard lock — allows edits with confirmation
    } catch(e) {
      // Skip if protection fails
    }
  });
}

// ─────────────────────────────────────────────
// UTILITY
// ─────────────────────────────────────────────
function formatDate(date) {
  var y = date.getFullYear();
  var m = String(date.getMonth() + 1).padStart(2, '0');
  var d = String(date.getDate()).padStart(2, '0');
  return y + '-' + m + '-' + d;
}

// ─────────────────────────────────────────────
// HELPER — Add a single Audit_Log entry from any tab
// Call this from other scripts when making changes
// Usage: logAuditEntry(ss, 'OPTED_OUT', 'LE', 'Tyler PD', 'John Smith', 'Replied remove', 'Nate')
// ─────────────────────────────────────────────
function logAuditEntry(ss, actionTag, tabName, orgName, contactName, detail, who) {
  var auditSheet = ss.getSheetByName('Audit_Log');
  if (!auditSheet) {
    Logger.log('ERROR: Audit_Log tab not found');
    return;
  }
  var entry = [formatDate(new Date()), actionTag, tabName, orgName, contactName, detail, who];
  var lastRow = auditSheet.getLastRow();
  auditSheet.getRange(lastRow + 1, 1, 1, entry.length).setValues([entry]);
}
