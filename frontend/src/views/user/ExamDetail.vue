<template>
    <Navbar />
    <div>
        <h1>Exam Detail</h1>
        <p>Name: {{ exam.name }}</p>
        <p>Type: {{ exam.exam_type }}</p>
        <p>Status: {{ exam.status }}</p>
        <p>Description: {{ exam.description }}</p>
        <p>Course: {{ exam.course_name }}</p>
        <p>Duration: {{ exam.duration }} minutes</p>
        <p>Maximum marks: {{ exam.max_marks }}</p>
        <p>Examiner: {{ exam.examinor_name }}</p>
        <p>Slot creation start: {{ exam.examinor_slot_create_start_date }}</p>
        <p>Slot creation end: {{ exam.examinor_slot_create_end_date }}</p>
        <p>Booking start: {{ exam.booking_start_time }}</p>
        <p>Booking end: {{ exam.booking_end_time }}</p>
        <p>Exam start: {{ exam.exam_start_date }}</p>
        <p>Exam end: {{ exam.exam_end_date }}</p>

        <h2>Slots</h2>
        <table border="1">
            <thead>
                <tr>
                    <th>Slot date</th>
                    <th>Slot time</th>
                    <th>End</th>
                    <th>Seats left</th>
                    <th>Meeting</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="slot in exam.slots" :key="slot.id">
                    <td>{{ slot.slot_date }}</td>
                    <td>{{ slot.slot_time }}</td>
                    <td>{{ slot.end_time }}</td>
                    <td>{{ slot.available }}</td>
                    <td><a v-if="slot.meeting_link" :href="slot.meeting_link">Link</a></td>
                    <td>
                        <button v-if="!slot.booked && exam.booking_open && slot.available > 0" @click="bookSlot(slot.id)">Book</button>
                        <button v-if="slot.booked && exam.booking_open" @click="cancelSlot(slot.id)">Cancel</button>
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
import { useRoute } from 'vue-router'

const examination_id = useRoute().params.examination_id
const message = ref('')
const exam = ref({
    name: '',
    description: '',
    course_name: '',
    examinor_name: '',
    examinor_slot_create_start_date: '',
    examinor_slot_create_end_date: '',
    booking_start_time: '',
    booking_end_time: '',
    exam_start_date: '',
    exam_end_date: '',
    exam_type: '',
    status: '',
    duration: '',
    max_marks: '',
    booking_open: false,
    slots: []
})

const getExamDetail = async () => {
    const response = await axios.post(`http://127.0.0.1:5000/exam_detail/${examination_id}`, {
        user_id: localStorage.getItem('user_id')
    })
    exam.value = response.data.data
}

const bookSlot = async (slot_id) => {
    const response = await axios.post(`http://127.0.0.1:5000/book_slot/${slot_id}`, {
        user_id: localStorage.getItem('user_id')
    })
    message.value = response.data.message
    getExamDetail()
}

const cancelSlot = async (slot_id) => {
    const response = await axios.post(`http://127.0.0.1:5000/cancel_slot/${slot_id}`, {
        user_id: localStorage.getItem('user_id')
    })
    message.value = response.data.message
    getExamDetail()
}

onMounted(() => {
    getExamDetail()
})
</script>
