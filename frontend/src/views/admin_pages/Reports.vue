<template>
    <Navbar />
    <h1>Reports</h1>
    <div class="stats">
        <div class="stat"><strong>{{ report.courses }}</strong><span>Courses</span></div>
        <div class="stat"><strong>{{ report.exams }}</strong><span>Examinations</span></div>
        <div class="stat"><strong>{{ report.students }}</strong><span>Students</span></div>
        <div class="stat"><strong>{{ report.examinors }}</strong><span>Examiners</span></div>
        <div class="stat"><strong>{{ report.slots }}</strong><span>Slots</span></div>
        <div class="stat"><strong>{{ report.bookings }}</strong><span>Bookings</span></div>
    </div>
    <table>
        <thead>
            <tr>
                <th>Examination</th>
                <th>Type</th>
                <th>Status</th>
                <th>Bookings</th>
                <th>Average marks</th>
                <th>Results</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="exam in report.exam_rows" :key="exam.name">
                <td>{{ exam.name }}</td>
                <td>{{ exam.exam_type }}</td>
                <td>{{ exam.status }}</td>
                <td>{{ exam.bookings }}</td>
                <td>{{ exam.average_marks }}</td>
                <td>{{ exam.results_published ? 'Published' : 'Hidden' }}</td>
            </tr>
        </tbody>
    </table>
</template>
<script setup>
import Navbar from '../components/Navbar.vue'
import axios from 'axios'
import { ref, onMounted } from 'vue'

const report = ref({ courses: 0, exams: 0, students: 0, examinors: 0, slots: 0, bookings: 0, exam_rows: [] })
onMounted(async () => {
    const response = await axios.get('http://127.0.0.1:5000/reports')
    report.value = response.data.data
})
</script>
<style scoped>
.stats { display: flex; flex-wrap: wrap; gap: 12px; margin: 16px 24px; }
.stat { background: #fff; border: 1px solid #d1d5db; border-radius: 6px; padding: 16px 24px; min-width: 120px; }
.stat strong { display: block; font-size: 28px; }
</style>
