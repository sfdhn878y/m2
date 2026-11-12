<template>
    <Navbar />
    <div>
        <h1>My Booking</h1>
        <table border="1">
            <thead>
                <tr>
                    <th>Exam</th>
                    <th>Slot date</th>
                    <th>Slot time</th>
                    <th>Status</th>
                    <th>Marks</th>
                    <th>Remarks</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                <tr v-if="bookings.length === 0">
                    <td colspan="7">No booking</td>
                </tr>
                <tr v-for="booking in bookings" :key="booking.id">
                    <td>{{ booking.name }}</td>
                    <td>{{ booking.slot_date }}</td>
                    <td>{{ booking.slot_time }}</td>
                    <td>{{ booking.status }}</td>
                    <td>{{ booking.marks }}</td>
                    <td>{{ booking.remarks }}</td>
                    <td>
                        <a :href="'/exam_detail/' + booking.exam_id">View Detail</a>
                        <button v-if="booking.status === 'Booked' && booking.booking_open" @click="cancelSlot(booking.slot_id)">Cancel</button>
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
import { ref, onMounted } from 'vue'

const bookings = ref([])
const message = ref('')

const getBookings = async () => {
    const response = await axios.post('http://127.0.0.1:5000/my_booking', {
        user_id: localStorage.getItem('user_id')
    })
    bookings.value = response.data.data
}

const cancelSlot = async (slot_id) => {
    const response = await axios.post(`http://127.0.0.1:5000/cancel_slot/${slot_id}`, {
        user_id: localStorage.getItem('user_id')
    })
    message.value = response.data.message
    getBookings()
}

onMounted(() => {
    getBookings()
})
</script>
