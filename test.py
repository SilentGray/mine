import logging
import maps.field as field

logging.basicConfig(filename='mine.log',
                    level=logging.DEBUG,
                    filemode='w',
                    format='%(levelname)s >> %(message)s')

newMap = field.Field()
