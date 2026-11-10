<template>
    <Navbar />
    <div>
        <h1>View Slot</h1>
        <p v-if="exam_name">Examination: {{ exam_name }}</p>
        <p v-if="slots.length === 0">No slots</p>

        <table v-else border="1">
            <thead>
                <tr>
                    <th>Date</th>
                    <th>Time</th>
                    <th>Capacity</th>
                    <th>Examiner</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="slot in slots" :key="slot.id">
                    <td>{{ slot.slot_date }}</td>
                    <td>{{ slot.slot_time }}</td>
                    <td>{{ slot.capacity }}</td>
                    <td>{{ slot.examinor_name }}</td>
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
const exam_name = ref('')
const slots = ref([])

const fetch_slots = async () => {
    const response = await axios.get(`http://127.0.0.1:5000/provide_slot_details/${examination_id}`)
    slots.value = response.data.data
    exam_name.value = response.data.exam_name
}

onMounted(() => {
    fetch_slots()
})
</script>
