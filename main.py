    def generate_image(self):
        """Формирует отчет в виде графиков (изображение).
        :returns:
            file (.png): 'graph.png'
        """
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2)
        index = np.arange(len(self.dct_years_salary))
        index2 = np.arange(10)
        index_years = []
        values_all = []
        count_all = []
        city_ax3 = []
        city_salary = []
        count_by_prof = []
        values_by_prof = []
        city_parts = []
        num_parts = []
        for key in dict(self.dct_part[:10]).keys():
            city_parts.append(key)
            num_parts.append(dict(self.dct_part)[key])
        city_parts.append('Другие')
        num_other = 1 - sum(dict(self.dct_part[:10]).values())
        num_parts.append(num_other)
        for key in dict(self.dct_salary_by_sity[:10]).keys():
            city_ax3.append(key.replace(" ", "\n").replace("-", "-\n"))
            city_salary.append(dict(self.dct_salary_by_sity)[key])
        for value in self.dct_years_count.values():
            count_all.append(value)
        for value in self.dct_years_count_filt.values():
            count_by_prof.append(value)
        for value in self.dct_years_salary_filt.values():
            values_by_prof.append(value)
        for key in self.dct_years_salary.keys():
            index_years.append(key)
            values_all.append(self.dct_years_salary[key])

        ax1.set_title('Уровень зарплат по годам', fontsize=8)
        ax1.bar(index, values_all, 0.4, label='Средняя з/п')
        ax1.bar(index+0.4, values_by_prof, 0.4, label=f'з/п {profession_name.lower()}')
        ax1.set_xticks(index + 0.2, index_years, rotation=90)
        ax1.legend(loc=2)
        ax1.xaxis.set_tick_params(labelsize=8)
        ax1.yaxis.set_tick_params(labelsize=8)
        ax1.yaxis.grid(True)

        ax2.set_title('Количество вакансий по годам', fontsize=8)
        ax2.bar(index, count_all, 0.4, label='Количество вакансий')
        ax2.bar(index + 0.4, count_by_prof, 0.4, label=f'Количество вакансий {profession_name.lower()}')
        ax2.set_xticks(index + 0.2, index_years, rotation=90)
        ax2.legend(loc=1)
        ax2.xaxis.set_tick_params(labelsize=8)
        ax2.yaxis.set_tick_params(labelsize=8)
        ax2.yaxis.grid(True)

        ax3.set_title('Уровень зарплат по городам', fontsize=8)
        ax3.barh(index2, list(reversed(city_salary)), 0.6)
        ax3.set_yticks(index2, list(reversed(city_ax3)))
        ax3.xaxis.set_tick_params(labelsize=8)
        ax3.yaxis.set_tick_params(labelsize=6)
        ax3.xaxis.grid(True)

        ax4.set_title('Доля вакансий по городам', fontsize=8)
        ax4.pie(list(reversed(num_parts)), labels=list(reversed(city_parts)), textprops={'fontsize': 6})
        ax4.axis('equal')

        plt.tight_layout()
        plt.savefig('graph.png')

    def generate_pdf(self):
        """Формирует отчет в виде PDF-файла
        :returns:
            file (.pdf): 'report.pdf'
        """
        statistic_by_year = [[year, self.dct_years_salary[year], self.dct_years_salary_filt[year], self.dct_years_count[year],
                              self.dct_years_count_filt[year]] for year in self.dct_years_salary]
        statistic_by_city = [[city, dict(self.dct_salary_by_sity)[city]] for city in dict(self.dct_salary_by_sity)]
        statistic_parts = [[city, str(round(dict(self.dct_part)[city] * 100, 2))] for city in dict(self.dct_part)]

        env = Environment(loader=FileSystemLoader('template'))
        template = env.get_template("pdf_template.html")
        pdf_template = template.render({'profession': profession_name,
                                        'image_graph': r'C:\Users\1\Desktop\graph.png',
                                        'statistic_by_year': statistic_by_year, 'statistic_by_city': statistic_by_city,
                                        'statistic_parts': statistic_parts})
        config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
        pdfkit.from_string(pdf_template, 'report.pdf', configuration=config, options={"enable-local-file-access": ""})


file_name = input('Введите название файла: ')
profession_name = input('Введите название профессии: ')
dataset = DataSet(file_name, profession_name)
dct_years_salary, dct_years_count, dct_years_salary_filt, dct_years_count_filt, dct_salary_by_sity, dct_part = dataset.parse_csv()

report = Report(dct_years_salary, dct_years_count, dct_years_salary_filt, dct_years_count_filt, dct_salary_by_sity,
                dct_part)

user_choice = input('вакансии или статистика ?: ').lower()
if user_choice == 'вакансии':
    report.generate_image()
elif user_choice == 'статистика':
    report.generate_excel()
else:
    print('Неверный формат ввода')