Feature: Тестовое задание

  @threads
  @browser
  Scenario: Сбор информации о дивидендах
    When зайти на сайт "ru.investing.com"
    Then навести на "выпадающий список" "Котировки"
    Then навести на "выпадающий список" "Акции"
    And  нажать на "пункт" "Россия"
    Then перейти на страницу акции
    Then собрать дивиденды акции
    Then выгрузить "дивиденды" в "dividends.json"