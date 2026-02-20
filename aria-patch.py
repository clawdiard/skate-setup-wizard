import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Add aria-live region for step announcements (after progress div)
html = html.replace(
    '</div>\n\n    <!-- Step 0: Style -->',
    '</div>\n\n    <div id="step-announce" aria-live="polite" aria-atomic="true" class="sr-only" style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0,0,0,0);"></div>\n\n    <!-- Step 0: Style -->'
)

# 2. Add role="radiogroup" to options containers and aria-label
html = html.replace(
    '<div class="options" id="style-options"></div>',
    '<div class="options" id="style-options" role="radiogroup" aria-label="Riding style"></div>'
)
html = html.replace(
    '<div class="options" id="level-options">',
    '<div class="options" id="level-options" role="radiogroup" aria-label="Experience level">'
)

# 3. Add role="radio" + aria-checked + aria-label to level option cards
html = html.replace(
    '<div class="option" onclick="selectLevel(this, \'beginner\')">',
    '<div class="option" role="radio" aria-checked="false" aria-label="Beginner: Just starting out or getting back into it" tabindex="0" onclick="selectLevel(this, \'beginner\')" onkeydown="if(event.key===\'Enter\'||event.key===\' \'){event.preventDefault();selectLevel(this,\'beginner\')}">'
)
html = html.replace(
    '<div class="option" onclick="selectLevel(this, \'intermediate\')">',
    '<div class="option" role="radio" aria-checked="false" aria-label="Intermediate: Comfortable riding, learning new tricks" tabindex="0" onclick="selectLevel(this, \'intermediate\')" onkeydown="if(event.key===\'Enter\'||event.key===\' \'){event.preventDefault();selectLevel(this,\'intermediate\')}">'
)
html = html.replace(
    '<div class="option" onclick="selectLevel(this, \'pro\')">',
    '<div class="option" role="radio" aria-checked="false" aria-label="Pro / Advanced: Years of experience, pushing limits" tabindex="0" onclick="selectLevel(this, \'pro\')" onkeydown="if(event.key===\'Enter\'||event.key===\' \'){event.preventDefault();selectLevel(this,\'pro\')}">'
)

# 4. Add aria-label to range inputs
html = html.replace(
    '<input type="range" id="height" min="120" max="210" value="170" step="1">',
    '<input type="range" id="height" min="120" max="210" value="170" step="1" aria-label="Height in centimeters" aria-valuetext="170 cm">'
)
html = html.replace(
    '<input type="range" id="height-ft" min="3" max="6" value="5" step="1">',
    '<input type="range" id="height-ft" min="3" max="6" value="5" step="1" aria-label="Height feet">'
)
html = html.replace(
    '<input type="range" id="height-in" min="0" max="11" value="7" step="1">',
    '<input type="range" id="height-in" min="0" max="11" value="7" step="1" aria-label="Height inches">'
)
html = html.replace(
    '<input type="range" id="shoe" min="5" max="15" value="9" step="0.5">',
    '<input type="range" id="shoe" min="5" max="15" value="9" step="0.5" aria-label="Shoe size" aria-valuetext="US 9">'
)

# 5. Add aria-pressed to unit toggle buttons
html = html.replace(
    '<button class="active" onclick="setHeightUnit(\'metric\')">Metric (cm)</button>',
    '<button class="active" aria-pressed="true" onclick="setHeightUnit(\'metric\')">Metric (cm)</button>'
)
html = html.replace(
    '<button onclick="setHeightUnit(\'imperial\')">Imperial (ft/in)</button>',
    '<button aria-pressed="false" onclick="setHeightUnit(\'imperial\')">Imperial (ft/in)</button>'
)
html = html.replace(
    '<button class="active" onclick="setShoeUnit(\'us\')">US</button>',
    '<button class="active" aria-pressed="true" onclick="setShoeUnit(\'us\')">US</button>'
)
html = html.replace(
    '<button onclick="setShoeUnit(\'eu\')">EU</button>',
    '<button aria-pressed="false" onclick="setShoeUnit(\'eu\')">EU</button>'
)
html = html.replace(
    '<button onclick="setShoeUnit(\'uk\')">UK</button>',
    '<button aria-pressed="false" onclick="setShoeUnit(\'uk\')">UK</button>'
)

# 6. Add aria-label to progress dots container
html = html.replace(
    '<div class="progress" id="progress">',
    '<div class="progress" id="progress" role="navigation" aria-label="Wizard progress">'
)

# 7. Add step labels and aria-current to progress dots in updateProgress JS
old_update = """function updateProgress() {
      document.querySelectorAll('.progress .dot').forEach((d, i) => {
        d.className = 'dot' + (i < currentStep ? ' done' : '') + (i === currentStep ? ' current' : '');
      });
    }"""
new_update = """function updateProgress() {
      const stepNames = ['Style', 'Experience', 'Height', 'Shoe Size', 'Results', 'Comparison'];
      document.querySelectorAll('.progress .dot').forEach((d, i) => {
        d.className = 'dot' + (i < currentStep ? ' done' : '') + (i === currentStep ? ' current' : '');
        d.setAttribute('aria-label', 'Step ' + (i+1) + ': ' + stepNames[i] + (i === currentStep ? ' (current)' : i < currentStep ? ' (completed)' : ''));
        d.setAttribute('aria-current', i === currentStep ? 'step' : 'false');
      });
      // Announce step change
      const announce = document.getElementById('step-announce');
      if (announce) announce.textContent = 'Step ' + (currentStep+1) + ' of 5: ' + stepNames[currentStep];
    }"""
html = html.replace(old_update, new_update)

# 8. Update selectLevel to set aria-checked
old_select = """function selectLevel(el, level) {
      document.querySelectorAll('#level-options .option').forEach(o => o.classList.remove('selected'));
      el.classList.add('selected');
      selectedLevel = level;
      setTimeout(() => nextStep(), 300);
    }"""
new_select = """function selectLevel(el, level) {
      document.querySelectorAll('#level-options .option').forEach(o => { o.classList.remove('selected'); o.setAttribute('aria-checked', 'false'); });
      el.classList.add('selected');
      el.setAttribute('aria-checked', 'true');
      selectedLevel = level;
      setTimeout(() => nextStep(), 300);
    }"""
html = html.replace(old_select, new_select)

# 9. Update height slider input handler to set aria-valuetext
old_height_handler = """document.getElementById('height').addEventListener('input', e => {
      const cm = e.target.value;
      document.getElementById('height-display').textContent = `${cm} cm`;
    });"""
new_height_handler = """document.getElementById('height').addEventListener('input', e => {
      const cm = e.target.value;
      document.getElementById('height-display').textContent = `${cm} cm`;
      e.target.setAttribute('aria-valuetext', cm + ' cm');
    });"""
html = html.replace(old_height_handler, new_height_handler)

# 10. Update shoe display to set aria-valuetext
old_shoe = """function updateShoeDisplay() {
      const v = parseFloat(document.getElementById('shoe').value);
      const prefix = shoeUnit.toUpperCase();
      document.getElementById('shoe-display').textContent = `${prefix} ${v}`;
    }"""
new_shoe = """function updateShoeDisplay() {
      const v = parseFloat(document.getElementById('shoe').value);
      const prefix = shoeUnit.toUpperCase();
      document.getElementById('shoe-display').textContent = `${prefix} ${v}`;
      document.getElementById('shoe').setAttribute('aria-valuetext', prefix + ' ' + v);
    }"""
html = html.replace(old_shoe, new_shoe)

# 11. Update setHeightUnit to toggle aria-pressed
old_height_unit = """btns.forEach(b => b.classList.remove('active'));
      if (unit === 'metric') {
        btns[0].classList.add('active');"""
new_height_unit = """btns.forEach(b => { b.classList.remove('active'); b.setAttribute('aria-pressed', 'false'); });
      if (unit === 'metric') {
        btns[0].classList.add('active'); btns[0].setAttribute('aria-pressed', 'true');"""
html = html.replace(old_height_unit, new_height_unit)

html = html.replace(
    """} else {
        btns[1].classList.add('active');
        document.getElementById('height-metric').style.display = 'none';""",
    """} else {
        btns[1].classList.add('active'); btns[1].setAttribute('aria-pressed', 'true');
        document.getElementById('height-metric').style.display = 'none';"""
)

# 12. Update setShoeUnit to toggle aria-pressed  
old_shoe_unit = """btns.forEach(b => b.classList.remove('active'));
      const slider = document.getElementById('shoe');"""
new_shoe_unit = """btns.forEach(b => { b.classList.remove('active'); b.setAttribute('aria-pressed', 'false'); });
      const slider = document.getElementById('shoe');"""
html = html.replace(old_shoe_unit, new_shoe_unit)

html = html.replace(
    "btns[0].classList.add('active');\n        slider.min = 5;",
    "btns[0].classList.add('active'); btns[0].setAttribute('aria-pressed', 'true');\n        slider.min = 5;"
)
html = html.replace(
    "btns[1].classList.add('active');\n        slider.min = 36;",
    "btns[1].classList.add('active'); btns[1].setAttribute('aria-pressed', 'true');\n        slider.min = 36;"
)
html = html.replace(
    "btns[2].classList.add('active');\n        slider.min = 4.5;",
    "btns[2].classList.add('active'); btns[2].setAttribute('aria-pressed', 'true');\n        slider.min = 4.5;"
)

# 13. Update renderStyleOptions to add role/aria to dynamic style cards
old_render = """div.onclick = () => {
          document.querySelectorAll('#style-options .option').forEach(o => o.classList.remove('selected'));
          div.classList.add('selected');
          selectedStyle = s;
          setTimeout(() => nextStep(), 300);
        };"""
new_render = """div.setAttribute('role', 'radio');
        div.setAttribute('aria-checked', 'false');
        div.setAttribute('aria-label', s.name + ': ' + s.description);
        div.setAttribute('tabindex', '0');
        div.onclick = () => {
          document.querySelectorAll('#style-options .option').forEach(o => { o.classList.remove('selected'); o.setAttribute('aria-checked', 'false'); });
          div.classList.add('selected');
          div.setAttribute('aria-checked', 'true');
          selectedStyle = s;
          setTimeout(() => nextStep(), 300);
        };
        div.onkeydown = (e) => { if(e.key==='Enter'||e.key===' '){e.preventDefault();div.click();} };"""
html = html.replace(old_render, new_render)

# 14. Add aria-label to steps
for i, label in enumerate(['Riding Style', 'Experience Level', 'Height', 'Shoe Size', 'Results', 'Setup Comparison']):
    html = html.replace(
        f'<div class="step" id="step-{i}">',
        f'<div class="step" id="step-{i}" role="region" aria-label="{label}">'
    )
# Step 0 has 'active' class
html = html.replace(
    '<div class="step active" id="step-0">',
    '<div class="step active" id="step-0" role="region" aria-label="Riding Style">'
)

with open('index.html', 'w') as f:
    f.write(html)

print("ARIA patch applied successfully")
