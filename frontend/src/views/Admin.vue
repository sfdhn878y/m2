<template>
<Navbar />
<h1>Admin dashboard</h1>
<div class="stats">
  <div class="stat">
    <strong>{{ stats.courses }}</strong>
    <span>Courses</span>
  </div>
  <div class="stat">
    <strong>{{ stats.exams }}</strong>
    <span>Exams</span>
  </div>
  <div class="stat">
    <strong>{{ stats.students }}</strong>
    <span>Students</span>
  </div>
  <div class="stat">
    <strong>{{ stats.examinors }}</strong>
    <span>Examiners</span>
  </div>
</div>
<div class="links">
  <a href="/create_course">Create Course</a>
  <a href="/create_examination">Create examination</a>
  <a href="/create_examinor">Create examinor</a>
</div>
</template>
<script setup>
import Navbar from './components/Navbar.vue'
import { ref, onMounted } from 'vue'
import axios from 'axios'

const stats = ref({
  courses: 0,
  exams: 0,
  students: 0,
  examinors: 0
})

const get_stats = async () => {
  const response = await axios.post('http://127.0.0.1:5000/provide_admin_stats')
  stats.value = response.data.data
}

onMounted(() => {
  get_stats()
})
</script>

<style scoped>
.stats {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin: 16px 24px;
}
.stat {
  background: #fff;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  padding: 16px 24px;
  min-width: 140px;
}
.stat strong {
  display: block;
  font-size: 28px;
}
.stat span {
  color: #4b5563;
}
</style>