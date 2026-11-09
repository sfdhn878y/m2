<template>
    <div>
        <h1>Create Course</h1>
    </div>
    {{ responce_frontend }}
    <form @submit.prevent="createCourse">
        <input type="text" v-model="courseName" placeholder="Course Name">
        <input type="text" v-model="courseDescription" placeholder="Course Description">
        <input type="number" v-model="courseDuration" placeholder="Course Duration">
        <button type="submit">Create Course</button>
    </form>
</template>
<script setup>
import { ref } from 'vue';
const courseName = ref('');
const courseDescription = ref('');
const courseDuration = ref('');
const error = ref('')
const responce_frontend = ref('')
import axios from 'axios';

const createCourse = async () => {
    try{
        const response = await axios.post(
            "http://127.0.0.1:5000/create_course",
            {
                courseName: courseName.value,
                courseDescription: courseDescription.value,
                courseDuration: courseDuration.value,
            }
        )
        responce_frontend.value = response.data

    }catch(err){
        error.value = err.message;

    }
}
</script>