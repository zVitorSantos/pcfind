<!-- Subtotals.vue -->
<template>
  <div class="subtotals">
    <h2>Subtotal</h2>
    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>Componente</th>
            <th>À vista</th>
            <th>Parcelado</th>
            <th>R$</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(subtotal, index) in subtotals" :key="index">
            <td>{{ `${subtotal.component} ${subtotal.quantity > 1 ? `x${subtotal.quantity}` : ''}` }}</td>
            <td>{{ subtotal.subtotalCash }}</td>
            <td>{{ subtotal.subtotalInstallment }}</td>
            <td>
              <select v-model="subtotal.selectedPriceType"
                @change="updateSelectedPriceType(index, $event.target.value)">
                <option value="cash">À vista</option>
                <option value="installment">Parcelado</option>
              </select>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { computed, defineProps, defineEmits, watchEffect } from 'vue'

const props = defineProps({
  items: Array
})

// Mapeamento de nomes de componentes com correspondência flexível
const componentNames = {
  'placa mãe': 'Placa Mãe',
  'processador': 'Processador',
  'memória': 'Memória RAM',
  'hd': 'HD',
  'ssd': 'SSD',
  'placa de vídeo': 'Placa de Vídeo',
  'fonte': 'Fonte de Alimentação',
  'cooler': 'Cooler',
  'gabinete': 'Gabinete',
  'monitor': 'Monitor',
  'teclado': 'Teclado',
  'mouse': 'Mouse',
  'headset': 'Headset',
  'placa de rede': 'Placa de Rede',
  'placa de som': 'Placa de Som'
}

const findComponentName = (title) => {
  if (!title) {
    return title;
  }

  // Extrair o nome do componente do título
  const component = title.split(',')[0];

  const normalizedComponent = component.toLowerCase(); // Converter para minúsculas
  for (const key in componentNames) {
    const normalizedKey = key.toLowerCase(); // Converter para minúsculas
    if (normalizedComponent.includes(normalizedKey)) {
      // Se o componente for 'hd' ou 'ssd', retornar 'HD/SSD'
      if (normalizedKey === 'hd' || normalizedKey === 'ssd') {
        return 'HD/SSD';
      }
      return componentNames[key]; // Retornar o nome correspondente
    }
  }

  // Se não houver correspondência, retornar o nome do componente
  return component;
}

const subtotals = computed(() => {
  if (!props.items || props.items.length === 0) {
    return [];
  }

  return props.items.map(item => {
    const quantity = Number(item.quantity);
    const cashPrice = item.cashPrice ? parseFloat(item.cashPrice.toString().replace(',', '.')) * quantity : 0;
    const installmentPrice = item.installmentPrice ? parseFloat(item.installmentPrice.toString().replace(',', '.')) * quantity : 0;

    if (isNaN(quantity) || isNaN(cashPrice) || isNaN(installmentPrice)) {
      // Handle error...
      return null;
    }

    const componentDisplayName = findComponentName(item.title);

    return {
      ...item,
      component: componentDisplayName,
      subtotalCash: cashPrice,
      subtotalInstallment: installmentPrice,
      selectedPriceType: item.selectedPriceType
    }
  }).filter(item => item !== null)
})

const totalCash = computed(() => {
  if (!subtotals.value || subtotals.value.length === 0) {
    return 0;
  }

  return subtotals.value.reduce((total, item) => total + item.subtotalCash, 0)
})

const totalInstallment = computed(() => {
  if (!subtotals.value || subtotals.value.length === 0) {
    return 0;
  }

  return subtotals.value.reduce((total, item) => total + item.subtotalInstallment, 0)
})

const selectedTotal = computed(() => {
  if (!subtotals.value || subtotals.value.length === 0) {
    return 0;
  }

  return subtotals.value.reduce((total, item) => {
    return total + (item.selectedPriceType === 'cash' ? item.subtotalCash : item.subtotalInstallment)
  }, 0)
})

const emit = defineEmits(['updateItem', 'updateTotals', 'update:selectedPriceType'])

watchEffect(() => {
  emit('updateTotals', {
    totalCash: totalCash.value,
    totalInstallment: totalInstallment.value,
    selectedTotal: selectedTotal.value,
    subtotals: subtotals.value,
    items: props.items
  })
})

const updateSelectedPriceType = (index, selectedPriceType) => {
  emit('update:selectedPriceType', { index, selectedPriceType });
}
</script>

<style scoped>
.subtotals {
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 100%;
  margin: 0 auto;
}

.subtotals h2 {
  padding-top: 0;
  padding-bottom: 0.5rem;
  margin-top: 0;
  margin-bottom: 0;
}

.table-container {
  height: 350px;
  max-height: calc(5 * 70px);
  width: 100%;
  max-width: 100%;
  overflow: overlay;
  scrollbar-width: none;
}

/* Para navegadores baseados em WebKit */
.table-container::-webkit-scrollbar {
  display: none;
}

.subtotals .table-container {
  display: flex;
  flex-direction: column;
  max-width: 600px;
  gap: 1em;
  background-color: #1a1a1a;
  padding: 1em;
  border-radius: 8px;
  color: rgba(255, 255, 255, 0.87);
  border: 1px solid #646cff;
  margin-bottom: 1em;
  max-height: calc(5 * 70px);
}

.subtotals table {
  width: 100%;
  border-collapse: collapse;
}

.subtotals th,
.subtotals td {
  border: 1px solid #ddd;
  padding: 8px;
}

.subtotals th {
  padding-top: 12px;
  padding-bottom: 12px;
  text-align: left;
  background-color: #242424;
  color: white;
}

.subtotals th:nth-child(1),
.subtotals td:nth-child(1) {
  width: 100px;
}

.subtotals th:nth-child(4),
.subtotals td:nth-child(4) {
  width: 100px;
}
</style>