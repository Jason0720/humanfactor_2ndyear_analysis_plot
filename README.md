# humanfactor_2ndyear_analysis_plot
> 2차년도 임상실험 데이터 장면별 통계분석 그래프 추출기

## File Structures
```
- project
  ├ main.py
  ├ figure (result figure)
  ├ figure-old (result figure - before rivision)
  ├ data (using csv data)
  ├ .gitattributes
  ├ .gitignore
  └ README.md
```

## Explanation
* session_plot
  * X_axis = Session / Y_axis = SSQ score by symptoms
  * from csv
  * `4` files ('session_plot_index.png')
* scene_plot
  * X_axis = Scene indices / Y_axis = MOS
  * from csv
  * `12` files ('scene_plot_index.png')
* ssq_plot
  * X_axis = SSQ score / Y_axis = SSQ symptoms
  * Group = under 30 / upper 30
  * manual data input (not from csv)
  * `4` files ('ssq_plot_index.png')
* ssq_33_group_plot
  * X_axis = Session / Y_axis SSQ score by symptoms ()
  * Group = MSSQ low / middle / upper
  * from csv / manual p-value data input
  * `12` files ('ssq_33_group_plot_index.png')
* **font size parameter**
  * (x_label_size, y_label_size, x_ticks_size, y_ticks_size, legend_size, p_value_size, value_size, value_digits)
  