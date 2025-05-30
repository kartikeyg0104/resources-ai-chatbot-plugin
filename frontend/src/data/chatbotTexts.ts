import rawTexts from './chatbotTexts.json';

export const getChatbotText = (key: keyof typeof rawTexts): string => {
    return rawTexts[key];
};
