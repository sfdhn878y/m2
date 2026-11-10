<template>
    <Navbar />
    <div>
        <h1>View Booking</h1>
        <table border="1">
            <thead>
                <tr>
                    <th>Exam</th>
                    <th>Student</th>
                    <th>Slot date</th>
                    <th>Slot time</th>
                    <th>Marks</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                <tr v-if="bookings.length === 0">
                    <td colspan="6">No booking</td>
                </tr>
                <tr v-for="booking in bookings" :key="booking.id">
                    <td>{{ booking.name }}</td>
                    <td>{{ booking.student_name }}</td>
                    <td>{{ booking.slot_date }}</td>
                    <td>{{ booking.slot_time }}</td>
                    <td>{{ booking.marks }}</td>
                    <td>
                        <a :href="'/give_marks/' + booking.id">Give Marks</a>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script setup>
import Navbar from '../components/Navbar.vue'
import axios from 'axios'
import { ref, onMounted } from 'vue'

const bookings = ref([])

const getBookings = async () => {
    const response = await axios.post('http://127.0.0.1:5000/examinor_bookings', {
        examinor_id: localStorage.getItem('user_id')
    })
    bookings.value = response.data.data
}

onMounted(() => {
    getBookings()
})
</script>
