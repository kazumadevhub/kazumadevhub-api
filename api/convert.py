from fastapi import APIRouter, HTTPException

convert_router = APIRouter(
    prefix="/api",
    tags=["conversion"],
)

@convert_router.get("/convert")
async def convert_unit(value: float, from_unit: str, to_unit: str):
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()

    conversions = {
        'length': {
            'meter': 1.0,
            'kilometer': 0.001,
            'centimeter': 100.0,
            'millimeter': 1000.0,
            'mile': 0.000621371,
            'yard': 1.09361,
            'foot': 3.28084,
            'inch': 39.3701
        },
        'weight': {
            'kilogram': 1.0,
            'gram': 1000.0,
            'milligram': 1000000.0,
            'pound': 2.20462,
            'ounce': 35.274
        },
        'temperature': {
            'celsius': lambda x: x,
            'fahrenheit': lambda x: (x * 9/5) + 32,
            'kelvin': lambda x: x + 273.15
        }
    }

    conversion_type = None
    for ctype, units in conversions.items():
        if from_unit in units and to_unit in units:
            conversion_type = ctype
            break

    if not conversion_type:
        raise HTTPException(status_code=400, detail="Invalid conversion units")

    if conversion_type == 'temperature':
        if from_unit == 'celsius' and to_unit == 'fahrenheit':
            result = conversions['temperature']['fahrenheit'](value)
        elif from_unit == 'fahrenheit' and to_unit == 'celsius':
            result = (value - 32) * 5/9
        elif from_unit == 'celsius' and to_unit == 'kelvin':
            result = conversions['temperature']['kelvin'](value)
        elif from_unit == 'kelvin' and to_unit == 'celsius':
            result = value - 273.15
        elif from_unit == 'fahrenheit' and to_unit == 'kelvin':
            result = (value - 32) * 5/9 + 273.15
        elif from_unit == 'kelvin' and to_unit == 'fahrenheit':
            result = (value - 273.15) * 9/5 + 32
        else:
            raise HTTPException(status_code=400, detail="Invalid temperature conversion")
    else:
        base_value = value / conversions[conversion_type][from_unit]
        result = base_value * conversions[conversion_type][to_unit]

    return {
        "from": from_unit,
        "to": to_unit,
        "original_value": value,
        "converted_value": result,
    }