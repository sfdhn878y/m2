<template>
  <Navbar />
  <main class="home">
    <section class="hero">
      <p class="eyebrow">Examination portal</p>
      <h1>Plan courses, exams, and question banks in one place</h1>
      <p class="lead">
        This portal is for admins and examiners who set up courses, schedule
        examinations, assign examiners, and build question banks for each exam.
      </p>
      <div class="actions">
        <a class="btn primary" href="/login">Login</a>
        <a class="btn" href="/register">Register</a>
      </div>
    </section>

    <section class="details">
      <h2>What you can manage</h2>
      <div class="cards">
        <article>
          <h3>Courses</h3>
          <p>Create a course with a name, description, and duration in hours.</p>
          <a href="/manage_course">Manage courses</a>
        </article>
        <article>
          <h3>Examinations</h3>
          <p>
            Schedule an exam against a course, set examiner slot dates, booking
            windows, and the exam start and end dates.
          </p>
          <a href="/manage_examination">Manage examinations</a>
        </article>
        <article>
          <h3>Examiners</h3>
          <p>Add examiner accounts and block or unblock access when needed.</p>
          <a href="/manage_examinor">Manage examiners</a>
        </article>
        <article>
          <h3>Question bank</h3>
          <p>Add questions and marks for a specific examination from its row.</p>
          <a href="/manage_examination">Open an examination</a>
        </article>
      </div>
    </section>

    <section class="roles">
      <h2>Who uses it</h2>
      <ul>
        <li><strong>Admin</strong> — creates courses, examinations, and examiner accounts.</li>
        <li><strong>Examiner</strong> — is assigned to an exam and can be blocked from login.</li>
        <li><strong>Student</strong> — registers with a name, email, and password.</li>
      </ul>
    </section>
  </main>
</template>

<script setup>
import Navbar from './components/Navbar.vue'
</script>

<style>
body {
  margin: 0;
  background: #f3f6f4;
  color: #1a1a1a;
}
</style>

<style scoped>
.home {
  max-width: 960px;
  margin: 0 auto;
  padding: 24px 16px 48px;
  font-family: Arial, sans-serif;
  color: #1a1a1a;
}

.hero {
  background: #143d2a;
  color: #f4fff6;
  border-radius: 12px;
  padding: 32px 28px;
}

.eyebrow {
  margin: 0 0 8px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  font-size: 12px;
  color: #b7f5c4;
}

h1 {
  margin: 0 0 12px;
  font-size: 32px;
  line-height: 1.2;
}

.lead {
  margin: 0 0 20px;
  max-width: 640px;
  line-height: 1.5;
}

.actions {
  display: flex;
  gap: 12px;
}

.btn {
  display: inline-block;
  padding: 10px 16px;
  border-radius: 6px;
  text-decoration: none;
  background: #fff;
  color: #143d2a;
  font-weight: 600;
}

.btn.primary {
  background: #9be15d;
  color: #143d2a;
}

.details,
.roles {
  margin-top: 32px;
}

h2 {
  margin: 0 0 16px;
}

.cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

article {
  border: 1px solid #d7e3d8;
  border-radius: 10px;
  padding: 16px;
  background: #f7fbf7;
}

article h3 {
  margin: 0 0 8px;
}

article p {
  margin: 0 0 12px;
  line-height: 1.45;
}

article a,
.roles a {
  color: #0b6b32;
}

.roles ul {
  margin: 0;
  padding-left: 18px;
  line-height: 1.7;
}
</style>
