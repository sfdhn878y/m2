<template>
    <Navbar />
    <div>
        <h1>See Examination</h1>
        <table border="1">
            <thead>
                <tr>
                    <th>Exam</th>
                    <th>Slot date</th>
                    <th>Slot time</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="examination in examinations" :key="examination.id">
                    <td>{{ examination.name }}</td>
                    <td>{{ examination.slot_date }}</td>
                    <td>{{ examination.slot_time }}</td>
                    <td>
                        <a :href="'/exam_detail/' + examination.exam_id">View Detail</a>
                        <button @click="bookSlot(examination.id)">Book Slot</button>
                    </td>
                </tr>
            </tbody>
        </table>
        <p>{{ message }}</p>
    </div>
</template>

<script setup>
import Navbar from '../components/Navbar.vue'
import axios from 'axios'
import { onMounted, ref } from 'vue'

const examinations = ref([])
const message = ref('')

const getExaminations = async () => {
    const response = await axios.get('http://127.0.0.1:5000/user/getExaminations')
    examinations.value = response.data.data1
}

const bookSlot = async (slot_id) => {
    const response = await axios.post(`http://127.0.0.1:5000/book_slot/${slot_id}`, {
        user_id: localStorage.getItem('user_id')
    })
    message.value = response.data.message
}

onMounted(() => {
    getExaminations()
})
</script>
