<template>
    <Navbar />
    <div>
        <h1>Exam Detail</h1>
        <p>Name: {{ exam.name }}</p>
        <p>Description: {{ exam.description }}</p>
        <p>Course: {{ exam.course_name }}</p>
        <p>Examiner: {{ exam.examinor_name }}</p>
        <p>Slot creation start: {{ exam.examinor_slot_create_start_date }}</p>
        <p>Slot creation end: {{ exam.examinor_slot_create_end_date }}</p>
        <p>Booking start: {{ exam.booking_start_time }}</p>
        <p>Booking end: {{ exam.booking_end_time }}</p>
        <p>Exam start: {{ exam.exam_start_date }}</p>
        <p>Exam end: {{ exam.exam_end_date }}</p>
        <p>Slot open: {{ exam.slot_open }}</p>

        <h2>Slots</h2>
        <table border="1">
            <thead>
                <tr>
                    <th>Slot date</th>
                    <th>Slot time</th>
                    <th>Capacity</th>
                    <th>Booked by</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="slot in exam.slots" :key="slot.id">
                    <td>{{ slot.slot_date }}</td>
                    <td>{{ slot.slot_time }}</td>
                    <td>{{ slot.capacity }}</td>
                    <td>{{ slot.booked_by }}</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script setup>
import Navbar from '../components/Navbar.vue'
import axios from 'axios'
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const examination_id = useRoute().params.examination_id
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
    slot_open: false,
    slots: []
})

const getExamDetail = async () => {
    const response = await axios.get(`http://127.0.0.1:5000/admin_exam_detail/${examination_id}`)
    exam.value = response.data.data
}

onMounted(() => {
    getExamDetail()
})
</script>
