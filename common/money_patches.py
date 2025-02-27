from django.utils import numberformat

original_format = numberformat.format


def patched_number_format(
    number,
    decimal_sep,
    decimal_pos=None,
    grouping=0,
    thousand_sep="",
    force_grouping=False,  # noqa: FBT002
    use_l10n=None,
):
    """
    Fix for Django Money formatting in Arabic locale - django-money
    """
    str_number = str(number)

    if "\u200f" in str_number and "." in str_number:
        if "\xa0" in str_number:
            num_part, currency_part = str_number.split("\xa0", 1)

            if "." in num_part and num_part.count(".") > 1:
                parts = num_part.split(".")
                num_part = parts[0] + "." + parts[1]

            formatted_num = original_format(
                num_part,
                decimal_sep,
                decimal_pos,
                grouping,
                thousand_sep,
                force_grouping,
                use_l10n,
            )

            return f"{formatted_num}\xa0{currency_part}"

    return original_format(
        str_number,
        decimal_sep,
        decimal_pos,
        grouping,
        thousand_sep,
        force_grouping,
        use_l10n,
    )


numberformat.format = patched_number_format
