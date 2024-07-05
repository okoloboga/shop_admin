###########
# Buttons #
###########

button-add-row = ✅ Добавить товар ✅
button-confirm = ✅ Подтверждаю ✅
button-edit-row = 📝 Редактировать товар 📝
button-catalogue = 📜 Каталог 📜
button-great = 👌 Отлично! 👌
button-back = ◀️ Назад
button-next = Вперед ▶️
button-edit = 📝 Редактировать 📝
button-delete = ❌ Удалить ❌
button-orders = 🧾 Заказы 🧾
button-accept-order = ✅ Принять ✅
button-decline-order = ❌ Отклонить ❌


############
# Messages #
############


start = Приветсвую в интерфейсе 😇 Админа!

        ✅ Добавление новых позиций ✅
        📜 Просмотр текущего каталога 📜

item-list = 📜 Список доступных товаров 📜

# Add Row

add-row-main = Нажми ✅ <b>Добавить товар</b>
               что бы начать процесс добавления
               позиции в 🗂 базу данных.

               Или нажми ◀️ <b>Назад</b>
               что бы вернуться в главное меню

fill-category = Введи 📊 <b>Категорию Товара</b>

                Это может быть строка из букв и цифр

wrong-category = Введена неверная категория

fill-name = Введи 🏷 <b>Название Товара</b>

            Это может быть строка из букв и цифр

wrong-name = Введено неверное название

fill-description = Введи 📑 <b>Описание Товара</b>

                   Это может быть строка из букв и цифр

wrong-description = Введено неверное описание

fill-image = Введи 🔗 ссылку на 🏞 <b>Изображение Товара</b>
             Ссылка должна начинаться на <code>https://</code>
             и заканчиваться расширением изображения, например
             <code>.jpg</code>

             Пример ссылки на изображение с бананом:
             <code>https://fruitonline.ru/image/cache/catalog/ban1-800x1000.jpg</code>

wrong-image = Введена неверная ссылка

fill-price-count = Введи 💱 <b>Стоимость товара</b>
                   <b>Себестоимость</b> (закупочная цена)
                   и <b>Количество товара</b> через пробел.

                   Это должны быть целые числа, <b>Себестоимость</b>
                   не может быть выше чем <b>Стоимость товара</b>

                   Например:
                   <code>1000 750 5</code>

wrong-price-count = Введена неверная цена или количество

confirm-new-item = Проверь введенные данные!

                   📊 Категория Товара: <b>{ $category }</b>
                   🏷 Название Товара: <b>{ $name }</b>
                   📑 Описание Товара:
                   <b>{ $description }</b>

                   🏞 Ссылка на изображение:
                   { $image }

                   💲 Стоимость товара: <b>{ $sell_price }</b>
                   💲 Себестоимоть: <b>{ $self_price }</b>
                   ✖️ Количество товара: <b>{ $count }</b>

                   Если все врено - нажми
                   ✅ Подтверждаю ✅

item-complete = <b>Отлично!</b>

                Товар добавлен в базу данных
                и в пользовательский каталог!

                Можешь вернуться в главное меню или начать
                ввод <b>Нового Товара</b>

item-show = 📊 Категория: <b>{ $category }</b>
            🏷 Название: <b>{ $name }</b>
            📑 Описание:
            <b>{ $description }</b>

            🏞 Ссылка на изображение:
            { $image }

            💲 Стоимость: <b>{ $sell_price }</b>
            💲 Себестоимоть: <b>{ $self_price }</b>
            ✖️ Количество: <b>{ $count }</b>

# Edit Row

edit-menu = Для изменения напиши <code>#что_меняешь</code>
            и новое значение. Например, что бы поменять название
            напиши <code>#name Новое Название</code>

            📊 Категория - <code>#category</code> - { $category }
            🏷 Название - <code>#name</code> - { $name }
            📑 Описание - <code>#description</code> -
            { $description }
            🏞 Изображение - <code>#image</code> -
            { $image }
            💲 Стоимость - <code>#sell_price</code> - { $sell_price }
            💲 Себестоимость - <code>#self_price</code> - { $self_price }
            ✖️ Количество - <code>#count</code> - { $count }

delete-confirm = Ты уверен что хочешь удалить
                 этот товар?

                 📊 <b>{ $category }</b>
                 🏷 <b>{ $name }</b>
                 📑 <b>{ $description }</b>
                 🏞 { $image }

                 💲 Стоимость: <b>{ $sell_price }</b>
                 💲 Себестоимоть: <b>{ $self_price }</b>
                 ✖️ Количество: <b>{ $count }</b>

delete-complete = Удаление завершено!

changes-complete = Редактирование завершено!

wrong-changes = Введены неверный зарпрос на изменения

# Confirm Order

orders_list = 🧾 Список не подтвержденных <b>заказов</b> 🧾
        
selected-order = 🧾 Неподтвержденный <b>заказ</b> #{ $index }🧾

accept-order = 🧾 Подтверждаешь <b>заказ</b> #{ $index }?🧾

decline_order = 🧾 Отклоняешь <b>заказ</b> #{ $index }?🧾                

order-data = ⌚️ Дата и время создания: <code>{ $date_and_time }</code>
             🆔 покупатели: <code>{ $user_id }</code>
             @username покупателя: <code>@{ $username }</code>

             🏠 Адрес доставки: 
             <code>{ $delivery_address }</code>

             🏷 Товар: <code>{ $item_index } { $name }</code>
             <code>{ $category }</code>
             ✖️ Количество: <code>{ $count }</code>

             💲 Прибыль: <code>{ $income }</code>
             💲 Чистая прибыль: <code>{ $pure_income }</code>                                  






