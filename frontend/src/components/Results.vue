<!-- Results.vue -->
<template>
  <div class="results">
    <div class="totals">
      <div class="total">
        <label>À vista:</label>
        <div>{{ totalCashPrice }}</div>
      </div>
      <div class="total">
        <label>Parcelado:</label>
        <div>{{ totalInstallmentPrice }}</div>
      </div>
      <div class="total">
        <label>Selecionado:</label>
        <div>{{ selectedTotal }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, defineProps } from 'vue'

const props = defineProps({
  items: Array,
  subtotals: Array
})

const totalCashPrice = computed(() => {
  return props.subtotals.reduce((total, subtotal) => total + subtotal.subtotalCash, 0)
})

const totalInstallmentPrice = computed(() => {
  return props.subtotals.reduce((total, subtotal) => total + subtotal.subtotalInstallment, 0)
})

const selectedTotal = computed(() => {
  return props.items.reduce((total, item) => {
    const price = item.selectedPriceType === 'cash' ? parseFloat(item.cashPrice) : parseFloat(item.installmentPrice)
    return total + (price * parseFloat(item.quantity))
  }, 0)
})
</script>

<style scoped>
.totals {
  display: flex;
  justify-content: center;
  gap: 1rem;
}

.total {
  padding: 0.5rem;
  border: 1px solid #888;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.total label {
  font-size: 0.75rem;
}
</style>