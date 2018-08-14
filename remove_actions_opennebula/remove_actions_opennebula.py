from selenium import webdriver
import argparse


def cli():
    parser = argparse.ArgumentParser(description='Delete actions from OpenNebula VM.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument('-u', '--url', type=str, default='cloud.metacentrum.cz', help='URL to OpenNebula.')
    parser.add_argument('-p', '--protocol', type=str, default='https://', help='Web protocol.')
    parser.add_argument('-c', '--chromedriver', type=str, default='/usr/local/bin/chromedriver',
                        help='Path to chromedriver binary.')
    parser.add_argument('-a', '--actions', nargs='+', default=['terminate-hard'], help='Action types to remove.')
    parser.add_argument('username', type=str, help='OpenNebula username.')
    parser.add_argument('password', type=str, help='OpenNebula password.')
    parser.add_argument('vm_name', type=str, help='VM name.')

    args = vars(parser.parse_args())
    
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('--window-size=1920,1080')

    driver = webdriver.Chrome(executable_path=args['chromedriver'], chrome_options=options)
    driver.get('{}{}:{}@{}'.format(args['protocol'], args['username'], args['password'], args['url']))

    if '401' in driver.title:
        print('Invalid credentials (error 401).')
        exit()

    print('Logged in!')

    driver.find_element_by_id('check_remember').click()
    driver.find_element_by_id('login_btn').click()

    driver.implicitly_wait(5)
    driver.find_element_by_id('li_instances-top-tab').find_element_by_tag_name('a').click()
    driver.implicitly_wait(5)
    driver.find_element_by_id('li_vms-tab').find_element_by_tag_name('a').click()
    driver.implicitly_wait(5)
    driver.find_element_by_css_selector('button[data-toggle="dataTableVmsSearch-dropdown"]').click()
    driver.find_element_by_css_selector('input[search-field="NAME"]').send_keys(args['vm_name'])
    driver.find_element_by_css_selector('input[search-field="UNAME"]').send_keys(args['username'])
    driver.find_element_by_css_selector('button.advanced-search').click()
    driver.implicitly_wait(5)

    vm_table = driver.find_element_by_id('dataTableVms')
    if vm_table.find_element_by_css_selector('tbody tr:first-child td').text == 'No matching records found':
        print('No matching VMs found. Exiting...')
        exit()

    vm_table.find_element_by_css_selector('tbody tr:first-child').click()
    driver.implicitly_wait(5)
    driver.find_element_by_id('vm_actions_tab-label').click()
    driver.implicitly_wait(5)

    get_actions_table = lambda: driver.find_element_by_id('scheduling_actions_table')

    if get_actions_table().find_element_by_css_selector('tbody tr:first-child td').text == 'No actions to show':
        print('No actions for VM found. Exiting...')
        exit()

    to_remove = []

    for action in get_actions_table().find_elements_by_css_selector('tbody tr'):
        action_type = action.find_element_by_css_selector('td.action_row')
        datetime = action.find_element_by_css_selector('td.time_row')

        if action_type.text in args['actions']:
            to_remove.append({'id': action_type.find_element_by_xpath('../td/div/a').get_attribute('id'),
                              'type': action_type.text,
                              'datetime': datetime.text})

    if not to_remove:
        print('No matching actions ({}) were found'.format(args['actions']))
        exit()

    for action in to_remove:
        driver.find_element_by_id(action['id']).click()
        driver.implicitly_wait(5)
        print("Removed action '{}' sheduled at '{}'".format(action['type'], action['datetime']))
        driver.refresh()
        driver.implicitly_wait(5)
        driver.find_element_by_id('vm_actions_tab-label').click()

    print('Done! Exiting...')


if __name__ == "__main__":
    cli()
