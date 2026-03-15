from typing import Optional
from abc import ABC, abstractmethod


class Module(ABC):
    def __init__(
        self,
        class_name: Optional[str] = None,
        id_name: Optional[str] = None,
        input_type: Optional[str] = "text",
        placeholder: Optional[str] = "",
        label: Optional[str] = "",
        col_size: Optional[str] = "s6",
    ):
        self.class_name = class_name
        self.id_name = id_name or f"{self.class_name}_input"
        self.input_type = input_type
        self.placeholder = placeholder
        self.label = label
        self.col_size = col_size

    def create_input(
        self,
        id_name: str,
        input_type: str = "",
        placeholder: str = "",
        label: str = "",
        col_size: str = "s6",
        step: str = "",
    ) -> str:
        _id = id_name if id_name else self.id_name
        _type = input_type or self.input_type
        _placeholder = placeholder or self.placeholder
        _label = label or self.label
        _col_size = col_size or self.col_size
        _step = step
        return f"""
        <div class="input-field col {_col_size}">
          <input id="{_id}" name="{_id}" type="{_type}" class="validate" placeholder="{_placeholder}" step="{_step}">
          <label for="{_id}">{_label}</label>
        </div>
        """

    def create_button(self, text: str, onclick: str = "", href: str = "#!", is_submit: bool = False) -> str:
        if is_submit:
            return f'<button type="submit" class="waves-effect waves-light btn">{text}</button>'
        onclick_html = f' onclick="{onclick}"' if onclick else ""
        return f'<a href="{href}" class="waves-effect waves-light btn"{onclick_html}>{text}</a>'

    def create_checkbox(self, label_text: str, class_name: str = "", id_name: str = "", name: str = "", value: Optional[str] = None) -> str:
        _class_name = class_name or self.class_name
        checkbox_id = id_name or f"{_class_name}_checkbox"
        _name = name or self.class_name
        _value = value if value is not None else id_name

        return f"""
        <p>
          <label>
            <input type="checkbox" id="{checkbox_id}" name="{_name}" value="{_value}" />
            <span>{label_text}</span>
          </label>
        </p>
        """
    
    def create_switch(self, label_text: str, class_name: str = "", id_name: str = "") -> str:
        _class_name = class_name or self.class_name
        switch_id = id_name or f"{_class_name}_switch"
        
        return f"""
        <div class="switch">
            <label>Off<input type="checkbox" id="{switch_id}"><span class="lever"></span>On</label>
        </div>
        <label>{label_text}</label>
        """

    def create_select(self, options: list, select_label: str, class_name: str = "", id_name: str = "", col_size: str = "") -> str:
        _class_name = class_name or self.class_name
        select_id = id_name or f"{_class_name}_select"
        _col_size = col_size or self.col_size
        
        option_html = ""
        for opt in options:
            if isinstance(opt, str):
                option_html += f'<option value="{opt.lower()}">{opt}</option>'
            else:
                val, label = opt
                option_html += f'<option value="{str(val).lower()}">{label}</option>'

        return f"""
        <div class="input-field col {_col_size}">
          <select id="{select_id}" name="{select_id}">
            <option value="" disabled selected>Choose</option>
            {option_html}
          </select>
          <label>{select_label}</label>
        </div>
        """
    
    def create_date(self, date_label: str, class_name: str = "", id_name: str = "", col_size: str = "") -> str:
        _class_name = class_name or self.class_name
        date_id = id_name or f"{_class_name}_date"
        _col_size = col_size or self.col_size

        return f"""
        <div class="input-field col {_col_size}">
          <input type="text" class="datepicker" id="{date_id}" name="{date_id}">
          <label for="{date_id}">{date_label}</label>
        </div>
        """