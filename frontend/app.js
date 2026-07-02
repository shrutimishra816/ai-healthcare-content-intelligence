const errorBox = document.getElementById("errorBox");

// ---------- Tabs ----------
document.querySelectorAll(".tab").forEach((btn) => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".tab").forEach((b) => b.classList.remove("active"));
    document.querySelectorAll(".tab-panel").forEach((p) => p.classList.remove("active"));
    btn.classList.add("active");
    document.getElementById(`panel-${btn.dataset.tab}`).classList.add("active");
    errorBox.classList.add("hidden");
  });
});

function showError(msg) {
  errorBox.textContent = msg;
  errorBox.classList.remove("hidden");
  errorBox.scrollIntoView({ behavior: "smooth", block: "center" });
}

function escapeHtml(str) {
  if (str === undefined || str === null) return "";
  return String(str).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

async function callApi(url, options) {
  const res = await fetch(url, options);
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || "Request failed.");
  return data;
}

function scoreChip(label, value, max = 100) {
  const color = value >= 0.75 * max ? "#35D07F" : value >= 0.45 * max ? "#F5A623" : "#E85C4A";
  return `<div class="score-chip"><span class="val" style="color:${color}">${value}</span><span class="lbl">${label}</span></div>`;
}

// ---------- Content Gap ----------
document.getElementById("gapForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const site = document.getElementById("gapSite").value.trim();
  const competitor = document.getElementById("gapCompetitor").value.trim();
  const out = document.getElementById("gapResults");
  out.innerHTML = "<p class='panel-note'>Fetching both pages…</p>";
  try {
    const data = await callApi(`/api/gap-analysis?site_url=${encodeURIComponent(site)}&competitor_url=${encodeURIComponent(competitor)}`);
    const missing = data.missing_on_site;
    const section = (label, arr) =>
      arr.length
        ? `<div class="topic-col"><h3>${label}</h3><ul class="tag-list">${arr.map((t) => `<li class="missing">${escapeHtml(t)}</li>`).join("")}</ul></div>`
        : `<div class="topic-col"><h3>${label}</h3><p class="panel-note">Nothing missing here 🎉</p></div>`;
    out.innerHTML = `
      <div class="score-row">${scoreChip("Coverage vs Competitor", data.coverage_vs_competitor_pct)}</div>
      <div class="subhead">Missing on your site</div>
      <div class="topic-cols">
        ${section("Diseases", missing.diseases)}
        ${section("Treatments", missing.treatments)}
      </div>
      ${missing.departments.length ? `<div class="topic-col" style="margin-top:14px"><h3>Departments</h3><ul class="tag-list">${missing.departments.map((t) => `<li class="missing">${escapeHtml(t)}</li>`).join("")}</ul></div>` : ""}
      <p class="panel-note" style="margin-top:16px">${escapeHtml(data.note)}</p>
    `;
  } catch (err) {
    out.innerHTML = "";
    showError(err.message);
  }
});

// ---------- Keyword Clustering ----------
document.getElementById("clusterForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const keywords = document.getElementById("clusterKeywords").value;
  const pillar = document.getElementById("clusterPillar").value;
  const out = document.getElementById("clusterResults");
  out.innerHTML = "<p class='panel-note'>Clustering…</p>";
  try {
    const data = await callApi("/api/keyword-cluster", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ keywords, pillar }),
    });
    out.innerHTML = `
      <div class="subhead">Pillar: ${escapeHtml(data.pillar)} (${data.total_keywords} keywords)</div>
      ${data.clusters
        .map(
          (c) =>
            `<div class="cluster-block"><h4>${escapeHtml(c.intent)}</h4><ul class="tag-list">${c.keywords.map((k) => `<li>${escapeHtml(k)}</li>`).join("")}</ul></div>`
        )
        .join("")}
      <p class="panel-note">${escapeHtml(data.note)}</p>
    `;
  } catch (err) {
    out.innerHTML = "";
    showError(err.message);
  }
});

// ---------- Content Brief ----------
document.getElementById("briefForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const topic = document.getElementById("briefTopic").value;
  const content_type = document.getElementById("briefType").value;
  const brand = document.getElementById("briefBrand").value;
  const out = document.getElementById("briefResults");
  out.innerHTML = "<p class='panel-note'>Generating brief…</p>";
  try {
    const data = await callApi("/api/content-brief", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ topic, content_type, brand }),
    });
    out.innerHTML = `
      <table class="data-table">
        <tr><td>Title</td><td>${escapeHtml(data.title)}</td></tr>
        <tr><td>Meta description</td><td>${escapeHtml(data.meta_description)}</td></tr>
      </table>
      <div class="subhead">Heading structure</div>
      <ol class="rec-list">${data.heading_structure.map((h) => `<li>${escapeHtml(h)}</li>`).join("")}</ol>
      <div class="subhead">FAQs</div>
      <ol class="faq-list">${data.faqs.map((f) => `<li>${escapeHtml(f)}</li>`).join("")}</ol>
      <div class="subhead">Internal link suggestions</div>
      <ul class="rec-list">${data.internal_link_suggestions.map((l) => `<li>${escapeHtml(l)}</li>`).join("")}</ul>
      <div class="subhead">E-E-A-T checklist</div>
      <ul class="checklist">${data.eeat_checklist.map((l) => `<li>${escapeHtml(l)}</li>`).join("")}</ul>
      <div class="subhead">GEO readiness checklist</div>
      <ul class="checklist">${data.geo_readiness_checklist.map((l) => `<li>${escapeHtml(l)}</li>`).join("")}</ul>
      <div class="subhead">Schema (copy-paste ready)</div>
      <button class="copy-btn" data-copy="brief-schema">Copy JSON-LD</button>
      <pre class="code-block" id="brief-schema">${escapeHtml(JSON.stringify(data.schema, null, 2))}</pre>
      <p class="panel-note">${escapeHtml(data.external_reference_guidance)}</p>
    `;
    attachCopyButtons(out);
  } catch (err) {
    out.innerHTML = "";
    showError(err.message);
  }
});

// ---------- Schema Generator ----------
document.getElementById("schemaForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const schema_type = document.getElementById("schemaType").value;
  const name = document.getElementById("schemaName").value;
  const description = document.getElementById("schemaDescription").value;
  const extra = document.getElementById("schemaExtra").value;

  const fields = { name, description };
  if (schema_type === "MedicalCondition") fields.treatments = extra;
  if (schema_type === "Physician") fields.specialties = extra;
  if (schema_type === "MedicalOrganization") fields.specialties = extra;

  const out = document.getElementById("schemaResults");
  out.innerHTML = "<p class='panel-note'>Generating…</p>";
  try {
    const data = await callApi("/api/schema", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ schema_type, fields }),
    });
    out.innerHTML = `
      <button class="copy-btn" data-copy="raw-schema">Copy JSON-LD</button>
      <pre class="code-block" id="raw-schema">${escapeHtml(JSON.stringify(data, null, 2))}</pre>
    `;
    attachCopyButtons(out);
  } catch (err) {
    out.innerHTML = "";
    showError(err.message);
  }
});

// ---------- Content Review ----------
document.getElementById("reviewForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const text = document.getElementById("reviewText").value;
  const out = document.getElementById("reviewResults");
  out.innerHTML = "<p class='panel-note'>Reviewing…</p>";
  try {
    const data = await callApi("/api/content-review", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });
    const ts = data.trust_signals;
    out.innerHTML = `
      <div class="score-row">
        ${scoreChip("Overall", data.scores.overall_content_score)}
        ${scoreChip("Trust", data.scores.trust_score)}
        ${scoreChip("Entity Coverage", data.scores.entity_coverage_score)}
        ${scoreChip("Readability", data.readability.flesch_reading_ease)}
      </div>
      <table class="data-table">
        <tr><td>Word count</td><td>${data.word_count}</td></tr>
        <tr><td>Readability</td><td>${escapeHtml(data.readability.label)}</td></tr>
        <tr><td>Medical reviewer mentioned</td><td>${ts.medical_reviewer_mentioned ? "yes" : "no"}</td></tr>
        <tr><td>Date signal present</td><td>${ts.date_signal_present ? "yes" : "no"}</td></tr>
        <tr><td>Citation language present</td><td>${ts.citation_language_present ? "yes" : "no"}</td></tr>
        <tr><td>Disclaimer present</td><td>${ts.medical_disclaimer_present ? "yes" : "no"}</td></tr>
      </table>
      <div class="subhead">Entities found</div>
      <ul class="tag-list">${data.entity_coverage.entities_found.map((t) => `<li class="found">${escapeHtml(t)}</li>`).join("") || "<li>none detected</li>"}</ul>
      <div class="subhead">Recommendations</div>
      <ol class="rec-list">${data.recommendations.map((r) => `<li>${escapeHtml(r)}</li>`).join("")}</ol>
      <p class="panel-note" style="margin-top:16px">${escapeHtml(data.note)}</p>
    `;
  } catch (err) {
    out.innerHTML = "";
    showError(err.message);
  }
});

function attachCopyButtons(container) {
  container.querySelectorAll(".copy-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const target = document.getElementById(btn.dataset.copy);
      navigator.clipboard.writeText(target.textContent).then(() => {
        const original = btn.textContent;
        btn.textContent = "Copied!";
        setTimeout(() => (btn.textContent = original), 1500);
      });
    });
  });
}
