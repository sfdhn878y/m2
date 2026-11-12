<template>
    <Navbar />
    <h1>All Bookings</h1>
    <input v-model="query" placeholder="Search student or exam">
    <p>{{ message }}</p>
    <table>
        <thead>
            <tr>
                <th>Student</th>
                <th>Exam</th>
                <th>Date</th>
                <th>Time</th>
                <th>Status</th>
                <th>Examiner</th>
                <th>Action</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="booking in filtered" :key="booking.id">
                <td>{{ booking.student_name }}</td>
                <td>{{ booking.exam_name }}</td>
                <td><input type="date" v-model="booking.slot_date"></td>
                <td><input type="time" v-model="booking.slot_time"></td>
                <td>{{ booking.status }}</td>
                <td>
                    <select v-model="booking.examinor_id">
                        <option v-for="examinor in examinors" :key="examinor.id" :value="examinor.id">{{ examinor.name }}</option>
                    </select>
                </td>
                <td>
                    <button @click="reschedule(booking)">Reschedule</button>
                    <button @click="reassign(booking)">Reassign</button>
                    <select v-model="booking.move_slot_id">
                        <option value="">Move to slot</option>
                        <option v-for="slot in slotsFor(booking.exam_id)" :key="slot.id" :value="slot.id">{{ slot.slot_date }} {{ slot.slot_time }}</option>
                    </select>
                    <button @click="moveBooking(booking)">Move</button>
                </td>
            </tr>
        </tbody>
    </table>
</template>
<script setup>
import Navbar from '../components/Navbar.vue'
import axios from 'axios'
import { ref, computed, onMounted } from 'vue'

const bookings = ref([])
const slots = ref([])
const examinors = ref([])
const query = ref('')
const message = ref('')
const filtered = computed(() => {
    const text = query.value.toLowerCase()
    return bookings.value.filter(booking => booking.student_name.toLowerCase().includes(text) || booking.exam_name.toLowerCase().includes(text))
})
const slotsFor = (examId) => slots.value.filter(slot => String(slot.exam_id) === String(examId))

const load = async () => {
    const response = await axios.get('http://127.0.0.1:5000/all_bookings')
    bookings.value = response.data.data.map(booking => ({ ...booking, move_slot_id: '' }))
    slots.value = response.data.slots
    examinors.value = response.data.examinors
}
const reschedule = async (booking) => {
    const response = await axios.post(`http://127.0.0.1:5000/reschedule_slot/${booking.slot_id}`, {
        slot_date: booking.slot_date,
        slot_time: booking.slot_time,
        end_time: booking.end_time
    })
    message.value = response.data.message
}
const reassign = async (booking) => {
    const response = await axios.post(`http://127.0.0.1:5000/reassign_examiner/${booking.id}`, {
        examinor_id: booking.examinor_id
    })
    message.value = response.data.message
    load()
}
const moveBooking = async (booking) => {
    const response = await axios.post(`http://127.0.0.1:5000/reschedule_booking/${booking.id}`, {
        slot_id: booking.move_slot_id
    })
    message.value = response.data.message
    load()
}
onMounted(load)
</script>
