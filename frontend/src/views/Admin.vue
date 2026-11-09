<template>
ths si admn apgwe
<Navbar />

<a href="/create_course">Create Course</a>
<a href="/create_examination">Create examination</a>
<a href="/create_examinor">Create examinor</a>

</template>
<script setup>
import Navbar from './components/Navbar.vue'
</script>

<style scoped>
.admin{
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #333;
    color: #fff;
    padding: 10px;
    border-radius: 5px;
}
</style>