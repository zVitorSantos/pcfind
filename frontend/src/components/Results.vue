<!-- Results.vue -->
<template>
  <div class="results">
    <div class="totals">
      <div class="total">
        <label>À vista:</label>
        <div>{{ totalCash }}</div>
      </div>
      <div class="total">
        <label>Parcelado:</label>
        <div>{{ totalInstallment }}</div>
      </div>
      <div class="total">
        <label>Selecionado:</label>
        <div>{{ selectedTotal }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, toRefs } from 'vue'

const props = defineProps({
  totalCash: Number,
  totalInstallment: Number,
  selectedTotal: Number,
  subtotals: Array,
  items: Array
})

const { totalCash, totalInstallment, selectedTotal } = toRefs(props)
</script>

<style scoped>
.results {
  box-sizing: border-box;
  overflow: hidden;
}

.totals {
  display: flex;
  justify-content: center;
  gap: 1rem;
  box-sizing: border-box;
}

.total {
  padding: 0.5rem;
  border: 1px solid #888;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  box-sizing: border-box;
}

.total label {
  font-size: 0.75rem;
}
</style>