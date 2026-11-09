<template>
    <Navbar />
    <div>
        <h1>Manage Course</h1>

        <table border="1">
            <thead>
                <tr>
                    <th>Course ID</th>
                    <th>Course Name</th>
                    <th>Description</th>
                    <th>Duration</th>
                    <th>Action</th>
                </tr>
            </thead>

            <tbody>
                <tr v-for="course in course_data_list" :key="course.id">
                    <td>{{ course.id }}</td>
                    <td>{{ course.name }}</td>
                    <td>{{ course.description }}</td>
                    <td>{{ course.duration }}</td>
                    <td>
                        <button @click="edit_course(course.id)">Edit</button>
                        <button @click="delete_course(course.id)">Delete</button>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>
<script setup>
import Navbar from '../components/Navbar.vue'
import { useRouter } from 'vue-router'
import { ref, onMounted } from 'vue'
const router = useRouter()
import axios from 'axios'
const course_data_list = ref([])
const get_course_data = async () => {
    const response = await axios.post('http://127.0.0.1:5000/provide_course_details')
    course_data_list.value = response.data.data
}
const edit_course = async (id) => {
    router.push(`/edit_course/${id}`)
}
const delete_course = async (id) => {
    const response = await axios.post(`http://127.0.0.1:5000/delete_course/${id}`)
}

onMounted(() => {
    get_course_data()
})

</script>
