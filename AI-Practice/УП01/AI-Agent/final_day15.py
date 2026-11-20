import os
import logging
from typing import Optional, Union, List
from pydantic import BaseModel, Field

logging.basicConfig(filename="app.log", level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

successful_requests_count = 0

class AnalysisResultBasic(BaseModel):
    topic: str
    category: str
    difficulty: str
    summary: str

class AnalysisResultDetailed(BaseModel):
    topic: str
    category: str
    difficulty: str
    summary: str
    key_steps: List[str] = Field(default_factory=list)
    common_mistakes: List[str] = Field(default_factory=list)

def get_api_key() -> str:
    key = os.getenv("LLM_API_KEY")
    if not key:
        logger.warning("API ключ не найден. Включаем режим эмуляции для проверки логики.")
        return None
    return key

def analyze_text_with_llm(user_input: str, mode: str) -> Optional[Union[AnalysisResultBasic, AnalysisResultDetailed]]:
    cleaned_text = user_input.strip()
    if not cleaned_text:
        logger.warning("Пользователь отправил пустой ввод после strip(). Запрос отменен.")
        print("Ошибка: Ввод не может быть пустым.")
        return None

    logger.info(f"Получен непустой запрос. Длина текста: {len(cleaned_text)} символов. Режим: {mode}")

    try:
        api_key = get_api_key()
        
        if api_key:
            logger.info("API-ключ успешно получен из переменных окружения.")
            raise NotImplementedError("Реальный вызов API отключен для теста без ключа")
        else:
            logger.info("Режим эмуляции: используем тестовые данные вместо реального API.")

        if mode == "basic":
            target_model = AnalysisResultBasic
            fake_response = {
                "topic": "Чтение CSV в Pandas",
                "category": "Data Science",
                "difficulty": "Medium",
                "summary": "Для чтения CSV используется pd.read_csv(), пропуски обрабатываются fillna() или dropna()."
            }
        else:
            target_model = AnalysisResultDetailed
            fake_response = {
                "topic": "Чтение CSV в Pandas",
                "category": "Data Science",
                "difficulty": "Medium",
                "summary": "Для чтения CSV используется pd.read_csv(), пропуски обрабатываются fillna() или dropna().",
                "key_steps": [
                    "Импортировать pandas как pd",
                    "Загрузить файл через pd.read_csv('file.csv')",
                    "Проверить пропуски методом df.isna().sum()",
                    "Обработать пропуски: заполнить (fillna) или удалить (dropna)",
                    "Сохранить очищенный датасет"
                ],
                "common_mistakes": [
                    "Не указать кодировку (encoding='utf-8'), из-за чего файл не читается",
                    "Пытаться применить методы к результату read_csv без присваивания переменной",
                    "Удалять строки с пропусками без анализа, теряя важные данные"
                ]
            }

        result = target_model.model_validate(fake_response)
        logger.info("Успешный ответ получен (эмуляция).")
        
        global successful_requests_count
        successful_requests_count += 1
        logger.info(f"Счётчик успешных запросов обновлён: {successful_requests_count}")

        return result

    except ValueError as ve:
        logger.error(f"Критическая ошибка конфигурации: {ve}", exc_info=True)
        print(f"Ошибка конфигурации: {ve}")
        return None
    except Exception as e:
        logger.error(f"Техническая ошибка: {e}", exc_info=True)
        print("Произошла ошибка при обработке запроса. Проверьте app.log для деталей.")
        return None

def save_result_to_file(result: Union[AnalysisResultBasic, AnalysisResultDetailed], mode: str) -> None:
    try:
        with open("result.txt", "a", encoding="utf-8") as f:
            f.write("-" * 40 + "\n")
            f.write(f"Режим: {mode}\n")
            f.write(f"Тема: {result.topic}\n")
            f.write(f"Категория: {result.category}\n")
            f.write(f"Сложность: {result.difficulty}\n")
            f.write(f"Краткий ответ: {result.summary}\n")
            
            if mode == "detailed" and isinstance(result, AnalysisResultDetailed):
                f.write(f"Ключевые шаги: {', '.join(result.key_steps)}\n")
                f.write(f"Типичные ошибки: {', '.join(result.common_mistakes)}\n")
            
            f.write("-" * 40 + "\n\n")
        logger.info("Результат успешно сохранён в result.txt")
    except IOError as io_err:
        logger.error(f"Ошибка записи в файл result.txt: {io_err}", exc_info=True)
        print("Не удалось сохранить результат в файл.")

if __name__ == "__main__":
    print("Выберите режим работы:")
    print("1 - Базовый (basic): 4 поля")
    print("2 - Детальный (detailed): 6+ полей (шаги, ошибки)")
    
    mode_choice = input("Введите 1 или 2: ").strip()
    mode = "basic" if mode_choice == "1" else "detailed"

    user_input = input("\nВведите текст для анализа: ")

    result = analyze_text_with_llm(user_input, mode)

    if result:
        print("\n--- Результат анализа ---")
        print(f"Тема: {result.topic}")
        print(f"Категория: {result.category}")
        print(f"Сложность: {result.difficulty}")
        print(f"Краткий ответ: {result.summary}")
        
        if mode == "detailed" and isinstance(result, AnalysisResultDetailed):
            print("\n📋 Ключевые шаги:")
            for i, step in enumerate(result.key_steps, 1):
                print(f"{i}. {step}")
            print("\n⚠️ Типичные ошибки:")
            for err in result.common_mistakes:
                print(f"- {err}")

        print(f"\n✅ Всего успешных запросов сегодня: {successful_requests_count}")
        save_result_to_file(result, mode)
        print("\n💾 Результат также сохранён в файл result.txt (добавлен в конец файла).")
    else:
        print("Анализ не выполнен.")
