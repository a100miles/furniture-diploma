export const kzt = (n: number) => `${Math.round(n).toLocaleString("ru-RU")} ₸`;
export const label = (category: string) => category.replace(/_/g, " ").replace(/^\w/, (c) => c.toUpperCase());
