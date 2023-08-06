# coding=utf8

from collections import OrderedDict, defaultdict
from texttable import Texttable


def _search_suitable_rule(self, domain):
    """ First find a rule among the ones defined on the procurement order
    group; then try on the routes defined for the product; finally fallback
    on the default behavior """
    if self.warehouse_id:
        domain = expression.AND(
            [['|', ('warehouse_id', '=', self.warehouse_id.id), ('warehouse_id', '=', False)], domain])
    Pull = self.env['procurement.rule']
    res = self.env['procurement.rule']
    if self.route_ids:
        res = Pull.search(expression.AND([[('route_id', 'in', self.route_ids.ids)], domain]),
                          order='route_sequence, sequence', limit=1)
    if not res:
        product_routes = self.product_id.route_ids | self.product_id.categ_id.total_route_ids
        if product_routes:
            res = Pull.search(expression.AND([[('route_id', 'in', product_routes.ids)], domain]),
                              order='route_sequence, sequence', limit=1)
    if not res:
        warehouse_routes = self.warehouse_id.route_ids
        if warehouse_routes:
            res = Pull.search(expression.AND([[('route_id', 'in', warehouse_routes.ids)], domain]),
                              order='route_sequence, sequence', limit=1)
    if not res:
        res = Pull.search(expression.AND([[('route_id', '=', False)], domain]), order='sequence', limit=1)
    return res


def parent_locations(location):
    result = location.browse()
    while location:
        result |= location
        location = location.location_id
    return result


def by_company(company, product):
    warehouse = env['stock.warehouse'].search([('company_id', '=', company.id)], limit=1)
    # location = warehouse.lot_stock_id
    location = env.ref('stock.stock_location_customers')
    return search_suitable_rule(product, location=location, warehouse=warehouse)


def search_suitable_rule(product=None, location=None, warehouse=None):
    from collections import OrderedDict

    expression = odoo.osv.expression
    result = OrderedDict()

    location = location or env['stock.location']
    warehouse = warehouse or env['stock.warehouse']

    domain = [('location_id', 'in', parent_locations(location).ids)]

    if warehouse:
        domain = expression.AND([['|', ('warehouse_id', '=', warehouse.id), ('warehouse_id', '=', False)], domain])

    Pull = env['procurement.rule']

    if product:
        product_routes = product.route_ids | product.categ_id.total_route_ids
        if product_routes:
            result['Product'] = product_res = OrderedDict()
            for route in product_routes.sorted('sequence'):
                product_rules = Pull.search(expression.AND([[('route_id', 'in', route.ids)], domain]), order='route_sequence, sequence')
                if product_rules:
                    product_res[route] = product_rules

    warehouse_routes = warehouse.route_ids
    if warehouse_routes:
        result['Warehouse'] = warehouse_res = OrderedDict()
        for route in warehouse_routes.sorted('sequence'):
            warehouse_rules = Pull.search(expression.AND([[('route_id', 'in', route.ids)], domain]), order='route_sequence, sequence')
            if warehouse_rules:
                warehouse_res[route] = warehouse_rules

    global_rules = Pull.search(expression.AND([[('route_id', '=', False)], domain]), order='sequence')
    if global_rules:
        result['Global'] = global_rules

    return result


#######################
def selectable(route):
    if not route:
        return ''

    result = []

    if route.sale_selectable:
        result.append('sale')

    if route.product_selectable:
        result.append('product')

    if route.product_categ_selectable:
        result.append('category')

    if route.warehouse_selectable:
        result.append('warehouse')

    return u' '.join(result)


def procure_method(rule):
    if rule.procure_method == 'make_to_order':
        return 'order'
    elif rule.procure_method == 'make_to_stock':
        return 'stock'


def route_name(route):
    if not route:
        return False

    return u'{route.sequence: 2d}. {route.name} ({route.id}) [{selectable}], [{wh}]'.format(
        route=route, selectable=selectable(route), wh=route.warehouse_ids)


def warehouse_rules(warehouse):
    from collections import OrderedDict
    from odoo.osv import expression

    result = OrderedDict()

    env = warehouse.env

    # if isinstance(warehouse, int):
    #     warehouse = env['stock.warehouse'].browse(warehouse)

    if warehouse._name == 'res.company':
        warehouse = env['res.company'].search([('company_id', '=', warehouse.id)], limit=1)

    assert warehouse._name == 'stock.warehouse'

    rules = env['procurement.rule'].search([('warehouse_id', '=', warehouse.id)])
    
    locations = rules.mapped('location_id').sorted('id')
    routes = rules.mapped('route_id').sorted(lambda r: r.sequence if r.sequence else 999)

    no_route_rules = rules.filtered(lambda r: not r.route_id)
    if no_route_rules:
        routes = [route for route in routes] + [no_route_rules[0].route_id]

    for route in routes:
        result[route] = row = OrderedDict()
        for location in locations:
            row[location] = (rules.filtered(lambda r: r.route_id == route and r.location_id == location)
                             .sorted('sequence'))

        no_route_rules = (rules.filtered(lambda r: r.route_id == False and r.location_id == False)
                      .sorted('sequence'))

        if no_route_rules:
            row[False] = no_route_rules

    # for rule in rules.sorted(lambda r: (r.route_sequence if r.route_sequence else 999, r.sequence)):
    #     for
    #
    #     if rule.location_id not in result:
    #         result[rule.location_id] = OrderedDict()
    #
    #     if rule.route_id not in result[rule.location_id]:
    #         result[rule.location_id][rule.route_id] = env['procurement.rule']
    #
    #     result[rule.location_id][rule.route_id] |= rule

    return result


def print_warehouse_rules(line, user_ns):
    warehouse = eval(line, user_ns)
    result = warehouse_rules(warehouse)

    for location, routes in result.items():
        print ' ' * 0, location
        for route, rules in routes.items():
            print ' ' * 4, route
            for rule in rules:
                print ' ' * 8, rule
            print
        print


def format_record(record):
    # return u'{0.id}. {0.name}'.format(record)
    return u'{0.name} ({0.id})'.format(record)


def format_sequence_record(record):
    return u'{: >2}. {}'.format(record.sequence, format_record(record))


def format_location(location):
    return format_record(location)


def format_route(route, warehouse):
    string = format_sequence_record(route)

    route_warehouses = route.warehouse_ids
    if warehouse in route_warehouses:
        route_warehouses -= warehouse
        string += u' ✓'

    if route.company_id:
        string += u'\n    {}'.format(format_record(route.company_id))

    string += u'\n    {}'.format(selectable(route))

    for warehouse in route_warehouses:
        string += u'\n    {}'.format(format_record(warehouse))

    return string


def format_rule(rule):
    string = (format_sequence_record(rule)
              + u'\n    {} {}'.format(rule.action, procure_method(rule)))

    if rule.mto_rule_id or rule.mts_rule_id:
        string += u'\n    mto -> {}, mts -> {}'.format(rule.mto_rule_id.id, rule.mts_rule_id.id)

    if rule.location_src_id:
        string += u'\n    {} ->'.format(format_record(rule.location_src_id))

    return string


def print_warehouse_rules_table(line, user_ns):
    warehouse = eval(line, user_ns)
    result = warehouse_rules(warehouse)

    if not result:
        return

    locations = result.values()[0].keys()

    attrs = []
    attrs.append([''] + [format_location(location) for location in locations])

    for route, locations in result.items():
        row = [format_route(route, warehouse)]
        attrs.append(row)
        for location, rules in locations.items():
            row.append(u'\n\n'.join(map(format_rule, rules)))

    table = Texttable()

    table.set_deco(Texttable.HEADER | Texttable.VLINES | Texttable.HLINES)
    table.set_max_width(180)

    table.add_rows(attrs)

    print(table.draw())
