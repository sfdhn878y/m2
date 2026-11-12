<template>
    <Navbar />
    <h1>Search</h1>
    <form @submit.prevent="search">
        <input v-model="query" placeholder="Search students, examiners, exams, bookings">
        <button type="submit">Search</button>
    </form>
    <h2>Students</h2>
    <table>
        <tr v-for="student in result.students" :key="student.id"><td>{{ student.name }}</td><td>{{ student.email }}</td></tr>
    </table>
    <h2>Examiners</h2>
    <table>
        <tr v-for="examinor in result.examinors" :key="examinor.id"><td>{{ examinor.name }}</td><td>{{ examinor.email }}</td><td>{{ examinor.department }}</td></tr>
    </table>
    <h2>Examinations</h2>
    <table>
        <tr v-for="exam in result.exams" :key="exam.id"><td>{{ exam.name }}</td><td>{{ exam.exam_type }}</td><td>{{ exam.status }}</td></tr>
    </table>
    <h2>Bookings</h2>
    <table>
        <tr v-for="booking in result.bookings" :key="booking.id"><td>{{ booking.student_name }}</td><td>{{ booking.exam_name }}</td><td>{{ booking.status }}</td></tr>
    </table>
</template>
<script setup>
import Navbar from '../components/Navbar.vue'
import axios from 'axios'
import { ref } from 'vue'

const query = ref('')
const result = ref({ students: [], examinors: [], exams: [], bookings: [] })
const search = async () => {
    const response = await axios.post('http://127.0.0.1:5000/admin_search', { query: query.value })
    result.value = response.data
}
</script>
