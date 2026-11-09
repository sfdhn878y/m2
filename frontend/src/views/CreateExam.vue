<template>
    <div>
        <h1>Create Examination</h1>
    </div>
    {{ examinor_data_list }}
    <form @submit.prevent="createExam">
        <input type="text" v-model="examName" placeholder="Exam Name">
        <input type="text" v-model="examDescription" placeholder="Exam Description">
        <input v-model='examinor_slot_create_start_date' placeholder="Slot Start Time">
        <input v-model='examinor_slot_create_end_date' placeholder="Slot End Time">
        <input v-model='booking_start_time' placeholder="Booking Start Time">
        <input v-model='booking_end_time' placeholder="Booking End Time">
        <input v-model='exam_start_date' placeholder="Exam Date">
        <input v-model='exam_end_date' placeholder="Examinor Name">

        <select v-model="course_id">
            <option v-for="course in course_data_list" :key="course.id" :value="course.id">
                {{ course.name }}
            </option>
        </select>

        <select v-model="examinor_id">
            <option v-for="examinor in examinor_data_list" :key="examinor.id" :value="examinor.id">
                {{ examinor.name }}
            </option>
        </select>

        <button type="submit">Create Exam</button>
    </form>
    {{ responce_frontend }}
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const examinor_data_list = ref([]);
const course_data_list = ref([]);
const examName = ref('');
const examDescription = ref('');
const examinor_slot_create_start_date = ref('');
const examinor_slot_create_end_date = ref('');
const booking_start_time = ref('');
const booking_end_time = ref('');
const exam_start_date = ref('');
const exam_end_date = ref('');
const course_id = ref('');
const examinor_id = ref('');
const responce_frontend = ref('');

const examinor_data = async () => {
    const response = await axios.post(
        "http://127.0.0.1:5000/provide_examinor_details",
    )
    examinor_data_list.value = response.data.data

}

const course_data = async () => {
    const response = await axios.post(
        "http://127.0.0.1:5000/provide_course_details",
    )
    course_data_list.value = response.data.data
}

const createExam = async () => {
    const response = await axios.post(
        "http://127.0.0.1:5000/create_exam",
        {
           exam_name: examName.value,
           exam_description: examDescription.value,
           examinor_slot_create_start_date: examinor_slot_create_start_date.value,
           examinor_slot_create_end_date: examinor_slot_create_end_date.value,
           booking_start_time: booking_start_time.value,
           booking_end_time: booking_end_time.value,
           exam_start_date: exam_start_date.value,
           exam_end_date: exam_end_date.value,
           course_id: course_id.value,
           examinor_id: examinor_id.value,
        }
    )
    responce_frontend.value = response.data
}

onMounted(() => {
    examinor_data();
    course_data();
})
</script>

<style scoped></style>