<template>
    <Navbar />
    <h1>Manage Students</h1>
    <input v-model="query" placeholder="Search name or email">
    <table>
        <thead>
            <tr>
                <th>Name</th>
                <th>Email</th>
                <th>Blocked</th>
                <th>Action</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="student in filtered" :key="student.id">
                <td>{{ student.name }}</td>
                <td>{{ student.email }}</td>
                <td>{{ student.is_blocked }}</td>
                <td>
                    <button @click="block_student(student.id)">Block</button>
                    <button @click="unblock_student(student.id)">Unblock</button>
                </td>
            </tr>
        </tbody>
    </table>
</template>
<script setup>
import Navbar from '../components/Navbar.vue'
import axios from 'axios'
import { ref, computed, onMounted } from 'vue'

const students = ref([])
const query = ref('')
const filtered = computed(() => {
    const text = query.value.toLowerCase()
    return students.value.filter(student => student.name.toLowerCase().includes(text) || student.email.toLowerCase().includes(text))
})

const load = async () => {
    const response = await axios.get('http://127.0.0.1:5000/provide_students')
    students.value = response.data.data
}
const block_student = async (id) => {
    await axios.post(`http://127.0.0.1:5000/block_student/${id}`)
    load()
}
const unblock_student = async (id) => {
    await axios.post(`http://127.0.0.1:5000/unblock_student/${id}`)
    load()
}
onMounted(load)
</script>
