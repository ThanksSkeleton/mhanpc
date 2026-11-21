const students = window.students;
const list = document.getElementById('students');
const base = document.querySelector('base').href;
const gm = location.pathname.includes('/gm/');
const section = gm ? 'gm/students/' : 'students/';
const radios = [];

function show(student) {
  const portrait = document.getElementById('portrait');
  portrait.src = new URL('portraits/' + student.portrait, base).href;
  portrait.alt = student.hero + ' portrait';
  const hero = document.getElementById('hero');
  hero.textContent = student.hero;
  if (student.alternate) {
    const alternate = document.createElement('i');
    alternate.textContent = student.alternate;
    hero.append(' [', alternate, ']');
  }
  document.getElementById('power').textContent = student.power;
  document.getElementById('real-name').textContent = student.real;
  document.getElementById('playbook').textContent = student.playbook;
  if (gm) {
    document.getElementById('worst').textContent = student.worst;
    document.getElementById('best').textContent = student.best;
  }

  document.title = student.hero + ' | MHA NPCs';
  const description = `${student.real} · ${student.playbook}\nPower: ${student.power}` +
    (gm ? `\n${student.worst} → ${student.best}` : '');
  document.querySelector('meta[name="description"]').content = description;
  document.querySelector('meta[property="og:title"]').content = document.title;
  document.querySelector('meta[property="og:description"]').content = description;
  document.querySelector('meta[property="og:url"]').content = new URL(section + student.slug + '.html', base).href;
  document.querySelector('meta[property="og:image"]').content = portrait.src;
  document.querySelector('meta[property="og:image:alt"]').content = portrait.alt;
  radios[students.indexOf(student)].checked = true;
}

students.forEach((student, index) => {
  const label = document.createElement('label');
  const radio = document.createElement('input');
  radio.type = 'radio';
  radio.name = 'student';
  radio.value = String(index);
  radio.addEventListener('change', () => {
    history.pushState(null, '', new URL(section + student.slug + '.html', base));
    show(student);
  });
  radios.push(radio);

  const name = document.createElement('b');
  name.textContent = student.hero;
  const playbook = document.createElement('i');
  playbook.textContent = student.playbook;

  label.append(radio, ' - ', name, ' - ', playbook);
  list.append(label, document.createElement('br'));
});

function studentFromUrl() {
  const slug = location.pathname.match(/\/students\/([^/]+)\.html$/)?.[1];
  return students.find(student => student.slug === slug) || students[0];
}

window.addEventListener('popstate', () => show(studentFromUrl()));
show(studentFromUrl());
