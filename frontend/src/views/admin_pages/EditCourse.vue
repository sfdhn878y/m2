<template>
    <Navbar />
    <div>
        <h1>Edit Course</h1>
    </div>
    {{ response_frontend_1 }}
    <form>
        <input type="text"  placeholder="Course Name" v-model="course_name" />
        <input type="text"  placeholder="Course Description" v-model="course_description" />
        <input type="number"  placeholder="Course Duration" v-model="course_duration" />
        <button @click="edit_course">Update Course</button>
    </form>
</template>
<script setup>
import Navbar from '../components/Navbar.vue'
import { useRoute } from 'vue-router'
import { ref, onMounted } from 'vue'
import axios from 'axios'
const route = useRoute()
const id = route.params.id
const response_frontend = ref({})
const response_frontend_1 = ref('')
const course_name = ref('')
const course_description = ref('')
const course_duration = ref('')

const get_course_data_specific   = async () => {
    const response = await axios.post(`http://127.0.0.1:5000/get_course_data_specific/${id}`)
    response_frontend.value = response.data.data
    course_name.value = response_frontend.value.name
    course_description.value = response_frontend.value.description
    course_duration.value = response_frontend.value.duration
}
const edit_course = async () => {
    const response = await axios.post(`http://127.0.0.1:5000/edit_course/${id}`, 
    
    { 
        
        name: course_name.value,
        description: course_description.value,
        duration: course_duration.value 


    })
    response_frontend_1.value = response.data.message
}
onMounted(() => {
    get_course_data_specific()
})

</script>
<style scoped>
.edit-course{
    display: flex;
    justify-content: space-between;
    align-items: center;
}
</style>